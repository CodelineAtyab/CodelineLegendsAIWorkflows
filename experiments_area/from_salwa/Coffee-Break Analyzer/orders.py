
from functools import reduce

orders: list[dict[str,str,]   | int ]= [   
  {"name": "salwa", "drink": "Latte", "size_oz": 16},
  {"name": "ali", "drink": "Espresso", "size_oz": 8},
  {"name": "khalfan", "drink": "Cappuccino", "size_oz": 20},
  {"name": "Mona", "drink": "Americano", "size_oz": 12},
  {"name": "fatam", "drink": "Mocha", "size_oz": 16},]

print(orders)

#is larage function
def is_large(orders: dict[str,str | int ]) ->bool:

   return int(orders["size_oz"]) >= 16

print(is_large(orders[0]))
print(is_large(orders[1]))
print(is_large(orders[2]))
print(is_large(orders[3]))


#filters
large_orders:filter(dict[str,str | int ])=filter(is_large, orders)

# print(list(large_orders))





# map with lambda

formatted_orders = list(  # noqa: C417
    map(
        lambda order: f"{order['name']} – {order['drink']} ({order['size_oz']}oz)",
        large_orders,
    )
)

print(formatted_orders)

# reduce

total_volume: int = reduce(lambda total, order: total + int(order["size_oz"]),
    orders,
    0,
)
print(total_volume)