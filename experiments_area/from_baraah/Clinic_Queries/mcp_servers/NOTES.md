# MCP Training Notes

An MCP server provides tools that clients can discover and call.
A tool is a Python function exposed through the MCP protocol.
I built three servers: Booking, Pharmacy, and Medical Reports.
The client connects to these servers and performs operations using their tools.
I implemented the MCP server and client parts of the clinic diagram but skipped the AI agents, UI, database, authentication, and other infrastructure.
