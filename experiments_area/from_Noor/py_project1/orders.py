from functools import reduce
from typing import Any


# Data source
orders = [
    {"name": "Alex", "drink": "Latte", "size_oz": 16},
    {"name": "Sara", "drink": "Cappuccino", "size_oz": 12},
    {"name": "John", "drink": "Americano", "size_oz": 20},
    {"name": "Maya", "drink": "Mocha", "size_oz": 16},
    {"name": "Omar", "drink": "Espresso", "size_oz": 8},
]


# Check if an order is large
def is_large(order):
    return order["size_oz"] >= 16


# Filter large orders
large_orders = list(filter(is_large, orders))


# Format each large order
formatted_orders = list(map(
    lambda order: f'{order["name"]} - {order["drink"]} ({order["size_oz"]}oz)',
    large_orders,
))


print("Large drinks: ",formatted_orders)


# Calculate total ounces
total_volume = reduce(
    lambda total, order: total + order["size_oz"],
    orders,
    0,
)

print(f"Total volume: {total_volume} oz")


# Optional: filter + map using list comprehension
large_orders_lc = [
    f'{order["name"]} - {order["drink"]} ({order["size_oz"]}oz)'
    for order in orders
    if order["size_oz"] >= 16
]

print("List comprehension: ",large_orders_lc)