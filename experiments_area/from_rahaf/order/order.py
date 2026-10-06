from functools import reduce


# Coffee orders data
orders: list[dict[str, str | int]] = [
    {"name": "rahaf", "drink": "V60", "size_oz": 16},
    {"name": "Sara", "drink": "Americano", "size_oz": 12},
    {"name": "wajdan", "drink": "Cappuccino", "size_oz": 20},
    {"name": "Baraah", "drink": "Mocha", "size_oz": 16},
]

def is_large(order: dict[str, str | int]) -> bool:
    return int(order["size_oz"]) >= 16

large_orders: list[dict[str, str | int]] = list(
    filter(is_large, orders)
)

formatted_large_orders: list[str] = list(
    map(
        lambda order: (
            f'{order["name"]} – {order["drink"]} '
            f'({order["size_oz"]}oz)'
        ),
        large_orders,
    )
)

total_volume: int = reduce(
    lambda total, order: total + int(order["size_oz"]),
    orders,
    0,
)

print(formatted_large_orders)
print("Total volume:", total_volume, "oz")