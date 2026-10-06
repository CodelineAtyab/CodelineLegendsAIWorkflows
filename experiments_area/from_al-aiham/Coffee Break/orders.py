from functools import reduce

orders: list[dict]= [
                    {"name": "Aiham",      "drink": "Latte", "size_oz": 16},
                    {"name": "Abu Yousef", "drink": "Latte", "size_oz": 15},
                    {"name": "Shaheen",    "drink": "Latte", "size_oz": 17},
                    {"name": "Alkahali",   "drink": "Latte", "size_oz": 12},
                    {"name": "Alabri",     "drink": "Latte", "size_oz": 11},
                    {"name": "Yarob",      "drink": "Latte", "size_oz": 21},
                    ]

def is_large(order:dict):
    return order["size_oz"] >= 16

large_orders = list(filter(is_large,orders))



result = list(map(lambda order: f"{order["name"]} - {order["drink"]} ({order["size_oz"]}oz)",large_orders))

for i in result:
    print(i)

total = reduce(lambda x,y: x + y, map(lambda order:order["size_oz"], large_orders))

print(f"Total volume: {total}oz")