from coffee import make_coffee

result = make_coffee(
    101,
    "latte",
    "Alice",
    "soy_milk",
    "extra_shot",
    size="large",
    takeaway=True
)

expected = {
    "order_id": 101,
    "coffee_type": "latte",
    "customer_name": "Alice",
    "extras": ("soy_milk", "extra_shot"),
    "options": {
        "size": "large",
        "takeaway": True
    }
}

if result == expected:
    print("PASS")
else:
    print("FAIL")


try:
    exec('make_coffee(order_id=101, "latte", "Alice")')
    print("NEGATIVE TEST FAIL")
except SyntaxError:
    print("NEGATIVE TEST PASS")