# Notes

An MCP server is a program that exposes capabilities, such as tools, to other programs over the Model Context Protocol, so that an MCP client (for example an agent) can discover and use them in a standard way. A tool is a normal Python function registered on the server; its name, docstring and type hints become the description and input schema that clients see when they list and call it.

In the Clinic Queries diagram I built the three MCP servers (Booking, Pharmacy and Medical Reports) with their six tools, plus one small async client that stands in for the agents' MCP clients. I skipped the agents, UI, API gateway, auth, Temporal, Redis, Postgres, Qdrant and monitoring; the data is kept in memory instead of a database.
