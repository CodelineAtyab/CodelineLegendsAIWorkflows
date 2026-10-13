from coffee import make_coffee

# Positive test case: valid input
expected = {
    "order_id": 101,
    "coffee_type": "latte",
    "customer_name": "Alice",
    "extras": ("soy_milk", "extra_shot"),
    "options": {"size": "large", "takeaway": True},
}

result = make_coffee(
    101, "latte", "Alice",
    "soy_milk", "extra_shot",
    size="large", takeaway=True
)

if result == expected:
    print("PASS")
else:
    print("FAIL")
    print("expected:", expected)
    print("got:", result)

# Negative test case raises a SyntaxError
#print(make_coffee(order_id=101, "latte", "Alice"))
