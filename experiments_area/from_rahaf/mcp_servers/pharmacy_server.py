from fastmcp import FastMCP

mcp = FastMCP("Clinic Pharmacy Server")

inventory: dict[str, int] = {
    "Paracetamol": 120,
    "Ibuprofen": 40,
}


@mcp.tool
def view_inventory() -> dict[str, int]:
    """Return a copy of the current medicine inventory."""
    return inventory.copy()


@mcp.tool
def add_inventory(medicine: str, quantity: int) -> dict[str, int | str]:
    """Add a positive quantity of a medicine and return its updated stock."""
    if quantity <= 0:
        return {"error": "Quantity must be greater than zero"}

    inventory[medicine] = inventory.get(medicine, 0) + quantity
    return {"medicine": medicine, "stock": inventory[medicine]}


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8002)
