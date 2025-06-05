# Neo4j Employee Graph

__Link to this repo__
[github.com/neo4j-product-examples/neo4j-employee-graph](https://github.com/neo4j-product-examples/neo4j-employee-graph)
<img src="img/qr-code-to-repo.png" width="150" alt="QR code to repository">

This hands-on workshop guides you through building an agentic GraphRAG application and demonstrates the importance of knowledge graphs and graph DBs for grounding AI, particularly in today's new Agentic world with advanced reasoning and diverse tool utilization.

__Agentic GraphRAG Architecture__
![](img/graphrag-architecture.png)


## Use Case Example

We focus specifically on a human resources and talent use case where we consider building a knowledge assistant for skills analysis, search, and team formation.

You'll learn to build an employee knowledge graph using Neo4j, combining resume data and HRIS information while utilizing GraphRAG tools, including MCP tools and agents via Google ADK.

 

## Workshop Modules

### Module 1: Vector Search with Agents
Learn how to create document nodes with vector indexes in Neo4j and expose to vector search retrieval tools to support agents.

### Module 2: Graph Construction and Retrieval
Learn how to construct a simple starter knowledge graph from documents to help with agent retrieval tools and improve responses. You will learn how to think through creating a simple graph data model and see the process of entity extraction to populate the graph with the right data.
You will then leverage a Neo4j MCP server to expose natural language querying tools to improve responses as well as write your own Cypher expert tools.


### Module 3: Expanding Data Sources
Learn how you can easily expand to include new sources in a knowledge graph backed by a graph database.  We show how you can add structured data from a Human Resource Information System (HRIS) and connect it to people extracted from the previous unstructured resume docs from module 2.

You will then be able to access additional data to further improve responses and answer more questions.

