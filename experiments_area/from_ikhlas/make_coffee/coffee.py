def make_coffee(order_id, coffee_type, customer_name, *extras, **options):
    return {
        "order_id": order_id,
        "coffee_type": coffee_type,
        "customer_name": customer_name,
        "extras": extras,
        "options": options
    }

