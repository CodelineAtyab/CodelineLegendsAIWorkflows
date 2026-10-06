orders: list[dict] = [
    {"name": "Alex", "drink": "Latte", "size_oz": 16},
    {"name": "Alzulaikha", "drink": "Americano", "size_oz": 10},
    {"name": "Bader", "drink": "Mocha", "size_oz": 18},
    {"name": "Maryam", "drink": "Espresso", "size_oz": 8},
]

def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16

filtered_list  = list(filter(is_large, orders))

print(filtered_list)

result = list(
    map(
        lambda order: f'{order["name"]} - {order["drink"]} ({order["size_oz"]}oz)',
        filtered_list
    )
)

print(result)