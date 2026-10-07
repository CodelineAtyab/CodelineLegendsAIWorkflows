from functools import reduce

# Coffee orders

orders: list[dict] = [
    {"name": "Wajdan", "drink": "Latte", "size_oz": 16},
    {"name": "Hidaya", "drink": "Espresso", "size_oz": 8},
    {"name": "Rahaf", "drink": "Americano", "size_oz": 20},
]
print("\nAll Orders:", orders)


# Check if the drink is large
def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16


# Filter large orders
large_orders: list[dict] = list(filter(is_large, orders))
print("\nLarge Orders:", large_orders)


# Convert large orders into formatted strings
formatted_orders: list[str] = list(
    map(
        lambda order: f"{order['name']} – {order['drink']} ({order['size_oz']}oz)",
        large_orders,
    )
)
print("\nFormatted Large Orders:", formatted_orders)

# Calculate the total volume of all drinks
total_volume = reduce(lambda x, y: x + y["size_oz"], orders, 0)
print(f"\nTotal volume: {total_volume} oz")

# Select large orders and format them using one list comprehension
large_orders_lc: list[str] = [
    f"{order['name']} – {order['drink']} ({order['size_oz']}oz)"
    for order in orders
    if order["size_oz"] >= 16
]
print("\nLarge Orders (List Comprehension):", large_orders_lc)
