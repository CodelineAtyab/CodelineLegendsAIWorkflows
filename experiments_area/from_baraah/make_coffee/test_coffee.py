from coffee import make_coffee


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

