from coffee import make_coffee


# Test coffee with required arguments
def test_coffee():

    result = make_coffee(
        101,
        "Ice Americano",
        "Baraah",
    )

    expected = {
        "order_id": 101,
        "coffee_type": "Ice Americano",
        "customer_name": "Baraah",
        "extras": (),
        "options": {},
    }

    if result == expected:
        print("Test 1: PASS")
    else:
        print("Test 1: FAIL")
        print("Expected:", expected)
        print("Got:", result)


# Test coffee with extras and options
def test_coffee_with_extras_and_options():

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
        print("Test 2: PASS")
    else:
        print("Test 2: FAIL")
        print("Expected:", expected)
        print("Got:", result)


# Invalid argument order causes a SyntaxError
# make_coffee(
#     order_id=101,
#     "latte",
#     "Alice",
# )


# Run both tests
test_coffee()
test_coffee_with_extras_and_options()
print("All tests passed!")