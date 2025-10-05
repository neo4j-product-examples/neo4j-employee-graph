#!/usr/bin/env uv run python
"""
Aura Agent MCP Server

A Model Context Protocol server that wraps an authenticated API endpoint
for Aura Agent queries.
"""

import json
import logging
import os
from typing import Any, Dict, Optional
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP, Context

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("aura-agent")

# Global configuration variables
client_id: Optional[str] = None
client_secret: Optional[str] = None
endpoint_url: Optional[str] = None
bearer_token: Optional[str] = None


def _load_config():
    """Load configuration from .env file and environment variables"""
    global client_id, client_secret, endpoint_url

    # Load .env file if it exists
    load_dotenv()
    logger.info("Loaded .env file configuration")

    # Get configuration from environment variables
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    endpoint_url = os.getenv("ENDPOINT_URL")

    # Log environment variable status (without exposing sensitive values)
    logger.info(f"Environment variables read - CLIENT_ID: {'✓' if client_id else '✗'}, "
                f"CLIENT_SECRET: {'✓' if client_secret else '✗'}, "
                f"ENDPOINT_URL: {'✓' if endpoint_url else '✗'}")

    if not all([client_id, client_secret, endpoint_url]):
        raise ValueError(
            "Required configuration not found. Set environment variables or config file:\n"
            "CLIENT_ID, CLIENT_SECRET, ENDPOINT_URL"
        )


async def _get_bearer_token() -> None:
    """Get OAuth bearer token"""
    global bearer_token

    auth_url = "https://api.neo4j.io/oauth/token"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                auth_url,
                auth=(client_id, client_secret),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={"grant_type": "client_credentials"},
                timeout=30.0
            )
            response.raise_for_status()

            token_data = response.json()
            bearer_token = token_data.get("access_token")

            if not bearer_token:
                raise ValueError("No access token in response")

            logger.info("Bearer token successfully received and cached")

        except httpx.HTTPError as e:
            raise Exception(f"Failed to get bearer token: {e}")


async def _call_aura_agent_api(question: str) -> Dict[str, Any]:
    """Call the Aura Agent API endpoint"""
    global bearer_token

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                endpoint_url,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {bearer_token}"
                },
                json={"input": question},
                timeout=60.0
            )

            # If token expired, refresh and retry once
            if response.status_code == 401:
                bearer_token = None
                await _get_bearer_token()

                response = await client.post(
                    endpoint_url,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": f"Bearer {bearer_token}"
                    },
                    json={"input": question},
                    timeout=60.0
                )

            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            raise Exception(f"API call failed: {e}")


@mcp.tool
async def aura_agent(question: str, ctx: Context) -> str:
    """Submit a natural language question to the aura agent.

    Args:
        question: Natural language question for the Aura Agent
        ctx: FastMCP context for logging and debugging

    Returns:
        JSON response from the Aura Agent API
    """
    global bearer_token

    try:
        await ctx.debug(f"Processing question: {question}")

        # Get bearer token if not already cached
        if not bearer_token:
            await _get_bearer_token()

        # Call the contract review API
        response = await _call_aura_agent_api(question)

        return json.dumps(response, indent=2)

    except Exception as e:
        await ctx.error(f"Aura Agent error: {str(e)}")
        raise Exception(f"Error: {str(e)}")


def main():
    """Main entry point"""
    # Load configuration
    _load_config()

    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main()