
def make_coffee(order_id, coffee_type, customer_name):
    return {
        "order_id": order_id,
        "coffee_type": coffee_type,
        "customer_name": customer_name,
    }

print(make_coffee(101, "latte", "Alice"))

def make_coffee(order_id, coffee_type, customer_name, *extras):
    print(extras)

make_coffee(101, "latte", "Alice", "soy_milk", "extra_shot")

make_coffee(101, "latte", "Alice")


def make_coffee(order_id, coffee_type, customer_name, *extras, **options):
    print(extras)
    print(options)

make_coffee(101, "latte", "Alice", "soy_milk", size="large", takeaway=True)

def make_coffee(order_id, coffee_type, customer_name, *extras, **options):
    return {
          "order_id": order_id,
         "coffee_type": coffee_type,
        "customer_name": customer_name,
         "extras": extras,
        "options": options,
    }
print(make_coffee(1, "espresso", "Bob"))
print(make_coffee(101, "latte", "Alice", "soy_milk", "extra_shot",
                  size="large", takeaway=True))
