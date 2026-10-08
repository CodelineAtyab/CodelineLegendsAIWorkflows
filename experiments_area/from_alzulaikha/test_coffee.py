from coffee import make_coffee

result = make_coffee(
    101,
    "v60",
    "Alzulaikha",
    "soy_milk",
    "extra_shot",
    size="large",
    takeaway=True
)

expected = {
    "order_id": 101,
    "coffee_type": "v60",
    "customer_name": "Alzulaikha",
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