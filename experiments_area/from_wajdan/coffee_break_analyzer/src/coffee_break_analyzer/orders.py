
# Coffee orders
orders: list[dict] = [
    {"name": "Wajdan", "drink": "Latte", "size_oz": 16},
    {"name": "Hidaya", "drink": "Espresso", "size_oz": 8},
    {"name": "Rahaf", "drink": "Americano", "size_oz": 20},
]
print(orders)

# Check if the drink is large
def is_large_order(order: dict) -> bool:
    return order["size_oz"] >= 16
