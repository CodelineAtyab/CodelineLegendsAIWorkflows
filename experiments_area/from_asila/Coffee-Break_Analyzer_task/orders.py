from functools import reduce

def main():
    print("Hello from coffee-break-analyzer-task!")


if __name__ == "__main__":
    main()

#list dictionary
orders: list[dict] = [{"name": "ALex" , "drink":"latte" , "size_oz":16} ,
                      {"name": "Asila" , "drink":"Matcha" , "size_oz":20},
                      {"name": "Suad" , "drink":"Americano" , "size_oz":12}]


def is_large(order:dict) -> bool:
    return order["size_oz"] >= 16 #  added quotation marks for (size_oz) because its a dictionary key 

#it filter orders by using (is_large function) and it save 
#and keep it inside large_orders
large_orders : list[dict] = list(filter(is_large, orders))

print(large_orders)
#inline lambda with map() to convert each order in large_orders into the string format
format_string: list[str] = list (
    map(
    lambda order: order["name"] +"– " + order["drink"] + str(order["size_oz"]) + "oz)", large_orders,
    )  # i used str(order["size_oz"]) becuase size_oz is a number, and (+) can only join strings with strings.
)
print(format_string)

#calculated total ounces ordered across all drinks and printed
total_ounces : int = reduce( lambda total , order:total + order ["size_oz"],orders,0)
print("Total volume: " + str(total_ounces) + " oz")

large_orders_lc: list[str] =[order["name"] + " - "  + order["drink"]+ " (" + str(order["size_oz"]) + "oz)"
    for order in orders
    if order["size_oz"]>= 16      
]

print(large_orders_lc)


