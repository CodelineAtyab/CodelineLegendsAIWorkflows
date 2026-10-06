import unittest

from coffee import make_coffee

class MakeCoffeeTests(unittest.TestCase): #The tests will be written inside this class

    def test_make_coffee_default(self): #test default result
        result = make_coffee(101, "americano", "Mohammed")
    
        print(result)
        
        self.assertEqual(
        result,
        {
            "order_id": 101,
            "coffee_type": "americano",
            "customer_name": "Mohammed",
            "extras": (),
            "options": {}
        }
    ) #after test This confirms that extras and options are empty when they are not provided


    def test_order_with_extras_and_options(self): #Test extras and options
        result = make_coffee(
        101,
        "latte",
        "Alice",
        "soy_milk",
        "extra_shot",
        size="large",
        takeaway=True
    )
        print(result)
        self.assertEqual(
        result,
        {
            "order_id": 101,
            "coffee_type": "latte",
            "customer_name": "Alice",
            "extras": ("soy_milk", "extra_shot"),
            "options": {
                "size": "large",
                "takeaway": True
            }
        }
    ) #This test checks that the extra coffee choices are saved correctly
    
    