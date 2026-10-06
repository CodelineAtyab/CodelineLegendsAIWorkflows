def make_coffee(order_id, coffee_type, customer_name, *extras, **options):
    print(f"Order ID: {order_id}")
    print(f"Coffee Type: {coffee_type}")
    print(f"Customer Name: {customer_name}")
    
    if extras:
        print("Extras:", extras)

    
    if options:
        print("Options:", options)


