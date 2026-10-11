
from coffee import make_coffee


def test_default_coffee():

    result = make_coffee(
        101,
        "V60",
        "rahaf"
    )

    expected = {
        "order_id": 101,
        "coffee_type": "V60",
        "customer_name": "rahaf",
        "extras": (),
        "options": {}
    }

    assert result == expected


def test_coffee_with_extras_and_options():

    result = make_coffee(
        101,
        "V60",
        "rahaf",
        "extra_shot",
        size="large",
        takeaway=True
    )

    expected = {
        "order_id": 101,
        "coffee_type": "V60",
        "customer_name": "rahaf",
        "extras": ("extra_shot"),
        "options": {
            "size": "large",
            "takeaway": True
        }
    }

    assert result == expected
