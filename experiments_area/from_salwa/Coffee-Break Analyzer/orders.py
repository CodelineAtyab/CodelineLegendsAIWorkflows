from functools import reduce

orders: list[dict] = [
    {"name": "salwa", "drink": "Latte", "size_oz": 16},
    {"name": "ali", "drink": "Espresso", "size_oz": 8},
    {"name": "khalfan", "drink": "Cappuccino", "size_oz": 20},
    {"name": "Mona", "drink": "Americano", "size_oz": 12},
    {"name": "fatam", "drink": "Mocha", "size_oz": 16},
]

# funcation is large
def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16

# Filter the large orders
large_orders = filter(is_large, orders)
# Format the large orders
formatted_orders = [
    f"{order['name']} - {order['drink']} ({order['size_oz']}oz)"
    for order in large_orders
]
print(formatted_orders)
# Calculate the total volume
total_volume = reduce(
    lambda total, order: total + order["size_oz"],
    orders,
    0,
)
print(f"Total volume: {total_volume} oz")
