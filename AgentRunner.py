from typing import Optional

from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai.types import UserContent, Part

#So I got annoyed copy-pasting the same code over and over in notebooks
# So I made a runner to wrap the adk runner...sorry
class AgentRunner:
    app_name: str
    user_id: str
    runner: InMemoryRunner
    session: Optional[Session]

    def __init__(self, app_name: str, user_id: str, agent: Agent):
        self.app_name = app_name
        self.user_id = user_id
        self.runner = InMemoryRunner(app_name=self.app_name, agent=agent)

    async def start_session(self):
        try:
            self.session = await self.runner.session_service.create_session(
                app_name=self.runner.app_name,
                user_id=self.user_id)
            print(f"Session started successfully with ID: {self.session.id}")
            return True
        except Exception as e:
            print(f"Error starting session: {str(e)}")
            raise e

    async def end_session(self):
        try:
            session_id = self.session.id
            await self.runner.session_service.delete_session(
                app_name=self.app_name,
                user_id=self.user_id,
                session_id=self.session.id)
            self.session = None
            print(f"Session {session_id} ended successfully")
            return True
        except Exception as e:
            print(f"Error ending session: {str(e)}")
            raise e

    async def restart_session(self):
        if self.session: await self.end_session()
        await self.start_session()

    async def run(self, new_message: str):
        if not self.session:
            raise Exception("No living session found. Please start a new session first with `start_session()`.")

        content = UserContent(parts=[Part(text=new_message)])
        result = None
        async for event in self.runner.run_async(
                user_id=self.session.user_id,
                session_id=self.session.id,
                new_message=content):
            for part in event.content.parts:
                print(part.text, part.function_call, part.function_response)
                if part.text:
                    result = part.text
        return result