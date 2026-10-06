from functools import reduce

# contains a hard-coded list[dict] named "orders"
# with the keys: name, drink, and size_oz

orders: list[dict] = [
    {"name": "Baraah", "drink": "Latte", "size_oz": 12},
    {"name": "Malak", "drink": "Americano", "size_oz": 8},
    {"name": "Fatma", "drink": "Ice Coffee", "size_oz": 18},
    {"name": "Rahaf", "drink": "V60", "size_oz": 20},
]


def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16


large_orders: list[dict] = list(filter(is_large, orders))

# convert the list of large orders into a list of formatted strings
orders_as_strings: list[str] = list(
    map(
        lambda order: f"{order['name']} - {order['drink']} ({order['size_oz']}oz)",
        large_orders,
    )
)

# calculate the total ounces ordered across all drinks
total_ounces: int = reduce(
    lambda x, y: x + y["size_oz"],
    orders,
    0,
)

print(orders_as_strings)
print("Total volume:", total_ounces, "oz")
