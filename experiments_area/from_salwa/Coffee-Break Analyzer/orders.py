
from functools import reduce

orders: list[dict[str,str,]   | int ]= [   
  {"name": "salwa", "drink": "Latte", "size_oz": 16},
  {"name": "ali", "drink": "Espresso", "size_oz": 8},
  {"name": "khalfan", "drink": "Cappuccino", "size_oz": 20},
  {"name": "Mona", "drink": "Americano", "size_oz": 12},
  {"name": "fatam", "drink": "Mocha", "size_oz": 16},]

print(orders)



#is larage function
def is_large(order: dict) -> bool:
    return order["size_oz"] >= 16


print(is_large(orders[0]))
print(is_large(orders[1]))
print(is_large(orders[2]))
print(is_large(orders[3]))


#filters
large_orders = filter(is_large, orders)


# Format the large orders
formatted_orders = list(
    map(
        lambda order: f"{order['name']} - {order['drink']} ({order['size_oz']}oz)",
        large_orders,
    )
)
print(formatted_orders)


# reduce
# Calculate the total volume
total_volume = reduce( lambda total, order: total + order["size_oz"],  orders, 0,)


print(f"Total volume: {total_volume} oz")