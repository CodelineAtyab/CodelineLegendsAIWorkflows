def make_coffee(order_id, coffee_type, customer_name, *extras, **options):
    """Create a coffee order and return it as a dictionary."""
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