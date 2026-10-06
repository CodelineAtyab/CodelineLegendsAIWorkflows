import unittest

from coffee import make_coffee


class TestMakeCoffee(unittest.TestCase):
    def test_default_order(self):
        result = make_coffee(101, "espresso", "Wajdan")

        self.assertEqual(result, {
            "order_id": 101,
            "coffee_type": "espresso",
            "customer_name": "Wajdan",
            "extras": (),
            "options": {},
        })

    def test_extras_and_options(self):
        result = make_coffee(
            101, "espresso", "Wajdan",
            "soy_milk", "extra_shot",
            size="large", takeaway=True,
        )

        self.assertEqual(result, {
            "order_id": 101,
            "coffee_type": "espresso",
            "customer_name": "Wajdan",
            "extras": ("soy_milk", "extra_shot"),
            "options": {
                "size": "large",
                "takeaway": True,
            },
        })

    def test_positional_after_keyword(self):
        invalid_code = 'make_coffee(order_id=101, "espresso", "Wajdan")'

        with self.assertRaises(SyntaxError):
            compile(invalid_code, "<test>", "exec")