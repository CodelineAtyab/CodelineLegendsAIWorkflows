from functools import reduce
from typing import Any, Dict, List

orders: List[Dict[str, Any]] = [
    {"name": "Alex", "drink": "Latte", "size_oz": 16},
    {"name": "Salim", "drink": "Espresso", "size_oz": 8},
    {"name": "Ahmed", "drink": "Mocha", "size_oz": 20},
]


def is_large(order: Dict[str, Any]) -> bool:
    """Return True if the order is 16 oz or larger."""
    return bool(order["size_oz"] >= 16)


large_orders: List[Dict[str, Any]] = list(filter(is_large, orders))

#  Convert each large order into a formatted string
formatted_orders: List[str] = list(
    map(
        lambda order: f"{order['name']} – {order['drink']} ({order['size_oz']}oz)",
        large_orders,
    )
)

total_oz: int = reduce(lambda acc, order: acc + order["size_oz"], orders, 0)

large_orders_lc: List[str] = [
    f"{o['name']} – {o['drink']} ({o['size_oz']}oz)" for o in orders if is_large(o)
]

for line in formatted_orders:
    print(line)

print(f"Total volume: {total_oz} oz")