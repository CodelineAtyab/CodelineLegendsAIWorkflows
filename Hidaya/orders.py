#Data Source 
orders: list[dict]= [
    {
        "name": "Alex",
        "drink": "Latte",
        "size_oz": 16,
     
    }
]

def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16

large_orders = filter(is_large, orders)

formatted_large_orders = list(map(lambda order: f"{order['name']} ordered a {order['size_oz']} oz {order['drink']}", large_orders))

print(formatted_large_orders)