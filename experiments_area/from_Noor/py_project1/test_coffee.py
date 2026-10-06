from CoffeeMachine import make_coffee


make_coffee(
    101, "latte", "Alice",
    "soy_milk", "extra_shot",
    size="large", takeaway=True
)

#after correction the syntax errors
make_coffee(order_id=101, coffee_type="latte", customer_name="Alice")
