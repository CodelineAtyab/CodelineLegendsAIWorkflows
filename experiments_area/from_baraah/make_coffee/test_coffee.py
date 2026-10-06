from coffee import make_coffee

import pytest


# Test coffee with only required arguments
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
        "options": {}
    }

    assert result == expected


# Test coffee with extras and options

def test_coffee_with_extras_and_options():

    result = make_coffee(
        101,
        "Ice Americano",
        "Baraah",
        "soy_milk",
        "extra_shot",
        size="large",
        takeaway=True
    )

    expected = {
        "order_id": 101,
        "coffee_type": "Ice Americano",
        "customer_name": "Baraah",
        "extras": ("soy_milk", "extra_shot"),
        "options": {
            "size": "large",
            "takeaway": True
        }
    }

    assert result == expected




# Test that invalid argument order raises a SyntaxError

def test_invalid():
    with pytest.raises(SyntaxError):
        exec('make_coffee(order_id=101, "Ice Americano", "Baraah")')