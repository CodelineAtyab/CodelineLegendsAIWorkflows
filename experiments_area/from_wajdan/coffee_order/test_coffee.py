from coffee import make_coffee

# Check an order without extras or options
result = make_coffee(101, "espresso", "Wajdan")

expected = {
    "order_id": 101,
    "coffee_type": "espresso",
    "customer_name": "Wajdan",
    "extras": (),
    "options": {},
}

if result == expected:
    print("Basic order: Passed")
else:
    print("Basic order: Failed")


# Check an order with extras and options
result = make_coffee(
    101,
    "latte",
    "Alice",
    "soy_milk",
    "extra_shot",
    size="large",
    takeaway=True,
)

expected = {
    "order_id": 101,
    "coffee_type": "latte",
    "customer_name": "Alice",
    "extras": ("soy_milk", "extra_shot"),
    "options": {
        "size": "large",
        "takeaway": True,
    },
}

if result == expected:
    print("Order with extras: Passed")
else:
    print("Order with extras: Failed")
