from fastmcp import FastMCP

mcp = FastMCP("Clinic Pharmacy Server")

inventory: dict[str, int] = {"Paracetamol": 120, "Ibuprofen": 40}


@mcp.tool
def view_inventory() -> dict:
    """Return the full pharmacy inventory as a dict of medicine name to stock."""
    return inventory


@mcp.tool
def add_inventory(medicine: str, quantity: int) -> dict:
    """Add stock for a medicine, creating it if it is new, and return its updated stock.

    Returns an error dict if the quantity is zero or negative.
    """
    if quantity <= 0:
        return {"error": "Quantity must be greater than 0"}
    inventory[medicine] = inventory.get(medicine, 0) + quantity
    return {"medicine": medicine, "stock": inventory[medicine]}


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8002)
