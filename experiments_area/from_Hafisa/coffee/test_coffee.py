from coffee import make_coffee


# Test 1 - Coffee without extras and options
def test_default_coffee():
    result = make_coffee(101, "V60", "Alice")

    expected = {
        "order_id": 101,
        "coffee_type": "V60",
        "customer_name": "Alice",
        "extras": (),
        "options": {}
    }

    assert result == expected
    print("Test 1 passed")


# Test 2 - Coffee with extras and options
def test_coffee_with_extras():
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

    assert result == expected
    print("Test 2 passed")




# Test 3 - Negative: keyword argument before positional arguments
# make_coffee(order_id=101, "latte", "Alice")
# SyntaxError: positional argument follows keyword argument


# Run the tests
if __name__ == "__main__":
    test_default_coffee()
    test_coffee_with_extras()
