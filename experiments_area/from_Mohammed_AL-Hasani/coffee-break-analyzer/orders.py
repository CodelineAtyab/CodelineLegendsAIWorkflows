from functools import reduce

orders: list[dict] = [{"name": "Alex", "drink": "Latte", "size_oz": 16},
                      {"name": "Jordan", "drink": "Cappuccino", "size_oz": 12},
                        {"name": "Taylor", "drink": "Espresso", "size_oz": 8},
                        {"name": "Morgan", "drink": "Americano", "size_oz": 20},
                        {"name": "Casey", "drink": "Mocha", "size_oz": 14 },
                        {"name": "Riley", "drink": "Flat White", "size_oz": 16}
                      ]

def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16

large_orders = list(filter(is_large, orders))

result = [f"{order['name']} - {order['size_oz']} oz {order['drink']}" for order in large_orders]

for i in result:
    print(i)
    
total = reduce(lambda x, y: x + y, [order["size_oz"] for order in orders])
print(f"Total volume: {total} oz")
