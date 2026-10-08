from functools import reduce


orders: list[dict] = [
    {"name": "Baraah", "drink": "Latte", "size_oz": 12},
    {"name": "Malak", "drink": "Americano", "size_oz": 8},
    {"name": "Fatma", "drink": "Ice Coffee", "size_oz": 18},
    {"name": "Rahaf", "drink": "V60", "size_oz": 20},
]


def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16


# Filter orders that are 16oz or larger
large_orders: list[dict] = list(filter(is_large, orders))


# Convert large orders into strings using lambda
orders_as_strings: list[str] = list(
    map(
        lambda order: f"{order['name']} - {order['drink']} ({order['size_oz']}oz)",
        large_orders,
    )
)


# Calculate total ounces of all orders
total_ounces: int = reduce(
    lambda x, y: x + y["size_oz"],
    orders,
    0,
)


print(orders_as_strings)
print("Total volume:", total_ounces, "oz")
