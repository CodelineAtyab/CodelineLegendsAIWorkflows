def make_coffee(order_id, coffee_type, customer_name, *extras, **options):
    print("order_id:", order_id)
    print("coffee_type:", coffee_type)
    print("customer_name:", customer_name)
    if extras == None:
        print("extras:", extras)

    if options == None:
        print("options:", options)

# make_coffee(101, "latte", "Alice")

make_coffee(
    101, "latte", "Alice",
    "soy_milk", "extra_shot",
    size="large", takeaway=True)