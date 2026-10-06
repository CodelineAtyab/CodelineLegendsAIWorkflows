import unittest
from coffee import make_coffee


class TestMakeCoffee(unittest.TestCase):

    def test_default_return(self):
        result = make_coffee(101, "v60", "Alzulaikha")

        expected = {
            "order_id": 101,
            "coffee_type": "v60",
            "customer_name": "Alzulaikha",
            "extras": (),
            "options": {}
        }

        self.assertEqual(result, expected)

    def test_extras_and_options(self):
        result = make_coffee(
            101,
            "v60",
            "Alzulaikha",
            "soy_milk",
            "extra_shot",
            size="large",
            takeaway=True
        )

        expected = {
            "order_id": 101,
            "coffee_type": "v60",
            "customer_name": "Alzulaikha",
            "extras": ("soy_milk", "extra_shot"),
            "options": {
                "size": "large",
                "takeaway": True
            }
        }

        self.assertEqual(result, expected)
