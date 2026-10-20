
from coffee import make_coffee

# Positive test
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


# Negative test
# make_coffee(order_id=101, "latte", "Alice")
# SyntaxError: positional argument follows keyword argument