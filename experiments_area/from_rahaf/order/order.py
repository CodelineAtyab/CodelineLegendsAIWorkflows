from functools import reduce


orders: list[dict[str, str | int]] = [
    {"name": "rahaf", "drink": "V60", "size_oz": 16},
    {"name": "Sara", "drink": "Americano", "size_oz": 12},
    {"name": "wajdan", "drink": "Cappuccino", "size_oz": 20},
    {"name": "Baraah", "drink": "Mocha", "size_oz": 16},
]

   
def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16


large_orders = list(filter(is_large, orders))


order_details = list(
    map(
        lambda order: f'{order["name"]} - {order["drink"]} ({order["size_oz"]} oz)',
        large_orders,
    )
)


total_ounces = reduce(
    lambda total, order: total + order["size_oz"],
    orders,
    0,
)


print(order_details)
print("Total ounces:", total_ounces)