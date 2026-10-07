from functools import reduce


orders: list[dict] = [
    {"name": "Baraah", "drink": "Latte", "size_oz": 12},
    {"name": "Malak", "drink": "Americano", "size_oz": 8},
    {"name": "Fatma", "drink": "Ice Coffee", "size_oz": 18},
    {"name": "Rahaf", "drink": "V60", "size_oz": 20},
]


def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16


def format_order(order: dict) -> str:
    return f"{order['name']} - {order['drink']} ({order['size_oz']}oz)"


large_orders: list[dict] = list(filter(is_large, orders))

orders_as_strings: list[str] = list(
    map(format_order, large_orders)
)

total_ounces: int = reduce(
    lambda x, y: x + y["size_oz"],
    orders,
    0,
)

print(orders_as_strings)
print("Total volume:", total_ounces, "oz")