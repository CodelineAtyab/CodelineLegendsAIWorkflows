from functools import reduce

 
orders: list[dict] = [
    {"name": "Alex", "drink": "Latte", "size_oz": 16},
    {"name": "Sara", "drink": "Espresso", "size_oz": 4},
    {"name": "Omar", "drink": "Cappuccino", "size_oz": 12},
    {"name": "Layla", "drink": "Mocha", "size_oz": 20},
    {"name": "Khalid", "drink": "Americano", "size_oz": 16},
    {"name": "Mona", "drink": "Flat White", "size_oz": 8},
]
 
 
def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16
large_orders = list(filter(is_large, orders))
#print(large_orders)

result = [f"{order['name']} - {order['drink']} ({order['size_oz']}oz)" for order in large_orders]
for i in result:
    print(i)

total_size = reduce(lambda x, y: x + y, (order["size_oz"] for order in orders))
print(f"Total size of all orders: {total_size} oz")
