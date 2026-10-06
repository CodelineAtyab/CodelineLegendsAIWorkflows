from coffee import make_coffee

# Order without extras
order = make_coffee(101, "espresso", "Wajdan")

expected = {
    "order_id": 101,
    "coffee_type": "espresso",
    "customer_name": "Wajdan",
    "extras": (),
    "options": {},
}

if order == expected:
    print("First test passed")
else:
    print("First test failed")


# Order with extras and options
order = make_coffee(
    101,
    "espresso",
    "Wajdan",
    "soy_milk",
    "extra_shot",
    size="large",
    takeaway=True,
)

expected = {
    "order_id": 101,
    "coffee_type": "espresso",
    "customer_name": "Wajdan",
    "extras": ("soy_milk", "extra_shot"),
    "options": {"size": "large", "takeaway": True},
}

if order == expected:
    print("Second test passed")
else:
    print("Second test failed")
