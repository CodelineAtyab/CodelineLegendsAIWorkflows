# Data Source
from functools import reduce


orders: list[dict] = [
    {"name": "Hidaya","drink": "Cappuccino","size_oz": 12,},
    {"name": "Rahaf", "drink": "Espresso", "size_oz": 8},
    {"name": "Alex","drink": "Latte","size_oz": 16,},
]


def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16

large_orders: filter[dict] = filter(is_large, orders)
formatted_large_orders: list[str] = list(map(lambda order: f"{order['name']} – {order['drink']} ({order['size_oz']}oz)",
        large_orders,))


total_ounces: int = reduce(lambda total, order: total + order["size_oz"], orders, 0)
for drink in formatted_large_orders:
    print(drink)
print("Total ounces sold: " + str(total_ounces) + " oz")
