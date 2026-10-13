from coffee import make_coffee

order = make_coffee(
    101, "latte", "Alice",
    "soy_milk", "extra_shot",
    size="large", takeaway=True,
)

expected = {
    "order_id": 101,
    "coffee_type": "latte",
    "customer_name": "Alice",
    "extras": ("soy_milk", "extra_shot"),
    "options": {"size": "large", "takeaway": True},
}

print("Test 1: PASS" if order == expected else "Test 1: FAIL")

# Test 2: Only required arguments
order = make_coffee(102, "espresso", "Hidaya")

expected = {
    "order_id": 102,
    "coffee_type": "espresso",
    "customer_name": "Hidaya",
    "extras": (),
    "options": {},
}

print("Test 2: PASS" if order == expected else "Test 2: FAIL")

# Test 3: Keyword argument before positional arguments (negative case)
# make_coffee(order_id=103, "latte", "Hidaya")
# SyntaxError: positional argument follows keyword argument