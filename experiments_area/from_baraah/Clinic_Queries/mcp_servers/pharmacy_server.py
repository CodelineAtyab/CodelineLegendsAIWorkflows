
from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Pharmacy MCP Server")

# Store medicines in memory
inventory = {
    "Paracetamol": 120,
    "Ibuprofen": 40,
}


@mcp.tool
def view_inventory() -> dict:
    """Return all medicines and their stock quantities."""
    return inventory.copy()


@mcp.tool
def add_inventory(medicine: str, quantity: int) -> dict:
    """Add medicine stock or create a new medicine."""

    # Reject invalid quantities
    if quantity <= 0:
        return {"error": "Quantity must be greater than zero"}

    # Add new medicine or increase existing stock
    inventory[medicine] = inventory.get(medicine, 0) + quantity

    return {
        "medicine": medicine,
        "stock": inventory[medicine],
    }


if __name__ == "__main__":
    mcp.run(transport="http", port=8002)
