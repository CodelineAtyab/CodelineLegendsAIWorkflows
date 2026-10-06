import pytest
from coffee import make_coffee

def test_coffee():

    result = make_coffee(
        101,
        "Ice Americano",
        "Hafisa"
    )

    assert result["order_id"] == 101
    assert result["coffee_type"] == "Ice Americano"
    assert result["customer_name"] == "Hafisa"
    assert result["extras"] == ()
    assert result["options"] == {}

def test_make_coffee():

    result = make_coffee(
        101,
        "latte",
        "Hafisa",
        "normal_milk",
        "single_shot",
        size="large",
        takeaway=True
    )

    assert result["order_id"] == 101
    assert result["coffee_type"] == "latte"
    assert result["customer_name"] == "Hafisa"
    assert result["extras"] == ("normal_milk", "single_shot")
    assert result["options"] == {"size": "large", "takeaway": True }


def test_invalid_argument_order():

    invalid_code = '''
make_coffee(
    order_id=101,
    "latte",
    "Hafisa"
)
'''

    with pytest.raises(SyntaxError):
        compile(invalid_code, "<string>", "exec")