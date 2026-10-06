from functools import reduce
from typing import TypedDict


class Order(TypedDict):
    name: str
    drink: str
    size_oz: int


orders: list[Order] = [{"name": "Mohammed", "drink": "Tea", "size_oz": 12}]


def is_large(order: Order) -> bool:
    return order["size_oz"] > 16


large_orders = list(filter(is_large, orders))

large_orders_strings = list(
    map(
        lambda order: f"{order['name']} - {order['drink']} ({order['size_oz']} oz)",
        large_orders,
    )
)

total_ounces = reduce(lambda total, order: total + order["size_oz"], orders, 0)
print(f"Total volume: {total_ounces} oz")
