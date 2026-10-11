from functools import reduce

orders: list[dict] = [
        {"name": "Alice", "drink": "Latte", "size_oz": 16},
        {"name": "Mohammed", "drink": "ColdBrew", "size_oz": 20},
        {"name": "Ahmed", "drink": "SpanishLatte", "size_oz": 25},
        {"name": "Sara", "drink": "Espresso", "size_oz": 8},
]

def is_large(order: dict) -> bool:
        """Return True when the drink is 16 oz or more."""
        return order["size_oz"] >= 16


large_orders: list[dict] = list(filter(is_large, orders))


large_lines: list[str] = list(
        map(
                lambda order: f"{order['name']} - {order['drink']} ({order['size_oz']}oz)",
                large_orders,
        )
)

print("Large drinks:")
for line in large_lines:
        print(line)


total_volume: int = reduce(lambda acc, order: acc + order["size_oz"], orders, 0)

print(f"Total volume: {total_volume} oz")


large_orders_lc: list[str] = [
        f"{order['name']} - {order['drink']} ({order['size_oz']}oz)"
        for order in orders
        if is_large(order)
]

print(f"List comprehension matches map + filter: {large_orders_lc == large_lines}")