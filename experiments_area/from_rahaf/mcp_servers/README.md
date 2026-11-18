# Clinic MCP servers

This project contains three FastMCP servers and small clients for practising the Clinic Queries tools. Start each server in its own terminal from this directory:

The uv configuration caps the transitive `cryptography` dependency below 49 so Intel Macs can install its available universal2 wheel without local OpenSSL build tools.

```sh
uv run booking_server.py
uv run pharmacy_server.py
uv run reports_server.py
```

Then, in another terminal, run `uv run clinic_client.py`. The warm-up server and client use port 8000; start `uv run hello_server.py` before running `uv run hello_client.py`.
