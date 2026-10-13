from functools import reduce


orders: list[dict] = [
    {"name": "Alex", "drink": "Latte", "size_oz": 16},
    {"name": "Alzulaikha", "drink": "Americano", "size_oz": 10},
    {"name": "Bader", "drink": "Mocha", "size_oz": 18},
    {"name": "Maryam", "drink": "Espresso", "size_oz": 8},
]


def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16

# Filter large coffee orders
filtered_list = list(filter(is_large, orders))

print(filtered_list)

# Format large orders using map and lambda
result = list(
    map(
        lambda order: f"{order['name']} - {order['drink']} ({order['size_oz']}oz)",
        filtered_list,
    )
)
# Format large orders using list comprehension
large_orders_lc = [
    f'{order["name"]} - {order["drink"]} ({order["size_oz"]}oz)'
    for order in orders
    if is_large(order)
]

print(result)

# Calculate the total volume of all drinks
total_volume = reduce(lambda total, order: total + order["size_oz"], orders, 0)
print(f"Total volume: {total_volume} oz")
