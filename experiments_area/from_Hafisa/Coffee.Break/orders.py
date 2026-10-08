from functools import reduce

orders: list[dict] = [
    {"name": "Alex", "drink": "Latte", "size_oz": 16},
    {"name": "Salim", "drink": "V60", "size_oz": 4},
    {"name": "Rahaf", "drink": "Espresso", "size_oz": 8},
]


def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16


large_orders = list(filter(is_large, orders))
formatted_orders = list(
    map(
        lambda order: f"{order['name']} – {order['drink']} ({order['size_oz']}oz)",
        large_orders,
    ),
)
total_volume = reduce(lambda total, order: total + order["size_oz"], orders, 0)
print("Large orders:")
for order in formatted_orders:
    print(order)
print("Total volume:", total_volume, "oz")
