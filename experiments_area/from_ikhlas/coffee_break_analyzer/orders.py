from functools import reduce

orders: list[dict] = [
                    {"name": "Alex", "drink": "latte", "size_oz": 16},
                    {"name": "Ikhlas", "drink": "Americano", "size_oz": 13},
                    {"name": "Wed", "drink": "v60", "size_oz": 20} 
                    ]

def is_large(order: dict) -> bool:
    if order["size_oz"]>=16:
        return True
    else:
        return False
print(is_large(orders[1]))


#using filter()
large_orders=list(filter(is_large, orders))
print(large_orders)


#using map() with lambda
order_format=list(map(lambda orders: f"{orders["name"]} - {orders["drink"]} ({orders["size_oz"]}oz)", large_orders))
print(order_format)


#using reduce()
total_ounces=reduce(lambda total, orders: total + orders["size_oz"], orders, 0)
print(f"Total volume: {total_ounces} oz")


#[Optional] Replicate the filter + map logic in one line via list-comprehension → large_orders_lc (for comparison).

combined_list_comp=[f"{order["name"]} - {order["drink"]} ({order["size_oz"]}oz)"
                     for order in orders 
                     if is_large(order)]
print(combined_list_comp)
