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
        "customer_name": "Baraah",
        "extras": (),
        "options": {}
    }

    assert result == expected


def test_coffee_with_extras():
    result = make_coffee(
        101,
        "latte",
        "Baraah",
        "soy_milk",
        "extra_shot",
        size="large",
        takeaway=True
    )

    expected = {
        "order_id": 101,
        "coffee_type": "latte",
        "customer_name": "Baraah",
        "extras": ("soy_milk", "extra_shot"),
        "options": {
            "size": "large",
            "takeaway": True
        }
    }

    assert result == expected



test_basic_coffee()
test_coffee_with_extras()
