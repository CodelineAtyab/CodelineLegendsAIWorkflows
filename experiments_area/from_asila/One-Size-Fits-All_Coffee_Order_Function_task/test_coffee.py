from coffee import make_coffee

result = make_coffee(101, "americano", "Mohammed")

# print(result)

expected_result = {
    "order_id": 101,
    "coffee_type": "americano",
    "customer_name": "Mohammed",
    "extras": (),
    "options": {},
}
# after test This confirms that extras and options are empty when they are not provided


# test_order_with_extras_and_options
result = make_coffee(
    101, "latte", "Alice", "soy_milk", "extra_shot", size="large", takeaway=True
)

expected_result = {
    "order_id": 101,
    "coffee_type": "latte",
    "customer_name": "Alice",
    "extras": ("soy_milk", "extra_shot"),
    "options": {"size": "large", "takeaway": True},
}

# This test checks that the extra coffee choices are saved correctly

if result == expected_result:
    print("Test 2 passed: extras and options are correct")
else:
    print("Test 2 failed: extras or options are incorrect")
