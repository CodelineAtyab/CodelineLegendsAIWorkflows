import unittest

from coffee import make_coffee


class TestMakeCoffee(unittest.TestCase): 

    # Only The three required arguments
    def test_default_order(self):
        result = make_coffee(101, "latte", "Alice")
        expected = {
            "order_id": 101,
            "coffee_type": "latte",
            "customer_name": "Alice",
            "extras": (),
            "options": {}
        }
        self.assertEqual(result, expected)

    # Required arguments plus extras and options
    def test_extras_and_options(self):
        result = make_coffee(
            101, "latte", "Alice",
            "soy_milk", "extra_shot",
            size="large", takeaway=True
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

        self.assertEqual(result, expected)

    # Invalid argument order must raise SyntaxError
    def test_invalid_argument_order(self):
        invalid_code = 'make_coffee(order_id=101, "latte", "Alice")'

        with self.assertRaises(SyntaxError):
            compile(invalid_code, "<test>", "exec")


if __name__ == "__main__":
    unittest.main()