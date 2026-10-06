from functools import reduce

orders: list[dict] = [
    {"name": "Alex", "drink": "Latte", "size_oz": 16},
    {"name": "Shaheen", "drink": "Latte", "size_oz": 10},
    {"name": "Mohammed", "drink": "Latte", "size_oz": 18},
    {"name": "Said", "drink": "Latte", "size_oz": 8},
    {"name": "Ali", "drink": "Latte", "size_oz": 16},
]


def is_large(order: dict):
        return order["size_oz"] >= 16


large_orders = list[dict](filter(is_large, orders))

print(large_orders)

result = map(
    lambda test: f"{test['name']} - {test['drink']} ({test['size_oz']} oz)",
    large_orders
)

print(list(result))


total_ounces = reduce(lambda total, order: total + order["size_oz"], large_orders, 0)

print(f"Total volume: {total_ounces} oz")
