from functools import reduce

orders: list[dict] = [
    {"name": "Mohammed", "drink": "Tea", "size_oz": 12},
    {"name": "Omar", "drink": "Soda", "size_oz": 16},
    {"name": "Huda", "drink": "Orange Juice", "size_oz": 20},
    {"name": "Fatima", "drink": "Zatar Laban Drink", "size_oz": 22},
]


def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16


large_orders: list[dict] = list(filter(is_large, orders))

# Issue #31 asks for map() with an inline lambda here, so ruff's C417
# (which would prefer a list comprehension) is switched off for this statement.
large_orders_strings: list[str] = list(  # noqa: C417
    map(
        lambda order: f"{order['name']} - {order['drink']} ({order['size_oz']} oz)",
        large_orders,
    )
)
print(f"Large orders: {large_orders_strings}")

total_ounces: int = reduce(lambda total, order: total + order["size_oz"], orders, 0)
print(f"Total volume: {total_ounces} oz")

# [Optional] the same filter + map logic in one line, for comparison
large_orders_lc: list[str] = [
    f"{order['name']} - {order['drink']} ({order['size_oz']} oz)"
    for order in orders
    if is_large(order)
]
