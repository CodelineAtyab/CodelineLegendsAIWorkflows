from coffee import make_coffee

make_coffee(
    101, "latte", "Alice", "soy_milk", "extra_shot", size="large", takeaway=True
)


# make_coffee(order_id=101, "latte", "Alice")
# I got this error after trying the above line: SyntaxError: positional argument follows keyword argument
