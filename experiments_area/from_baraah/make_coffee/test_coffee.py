from coffee import make_coffee


def test_basic_coffee():
    result = make_coffee(
        101,
        "latte",
        "Alice"
    )

    expected = {
        "order_id": 101,
        "coffee_type": "latte",
        "customer_name": "Alice",
        "extras": (),
        "options": {}
    }

    assert result == expected


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


def test_invalid_argument_order():
    invalid_code = '''
make_coffee(
    order_id=101,
    "latte",
    "Alice"
)
'''

    try:
        exec(invalid_code)
        assert False
    except SyntaxError:
        print("Negative test passed")


test_basic_coffee()
test_coffee_with_extras()
test_invalid_argument_order()