from coffee import make_coffee
def test_make_coffee():
    result = make_coffee(11, "latte", "Ikhlas")
    expected = {"order_id": 11,
                "coffee_type": "latte",
                "customer_name": "Ikhlas",
                "extras": (),
                "options": {}
    }
    if result == expected:
        print("first test passed")
    else:
        print("first test failed")
        print("Expected:", expected)
        print("Got:", result)
    return result

def test_make_coffee_with_extras():
    result = make_coffee(11,
                        "latte",
                        "Ikhlas",
                        "low_fat_milk",
                        "iced",
                        size="large",
                        takeaway=True)

    expected = {
        "order_id": 11,
        "coffee_type": "latte",
        "customer_name": "Ikhlas",
        "extras": ("low_fat_milk", "iced"),
        "options": {
            "size": "large",
            "takeaway": True
        }
    }

    if result == expected:
        print("second test passed")
    else:
        print("second test failed")

        print("Expected:", expected)
        print("Got:", result)

#to run the tests
test_make_coffee()
test_make_coffee_with_extras()