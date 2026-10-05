from coffee import make_coffee

# Positive test case: Valid input
print(make_coffee(
    101, "latte", "Alice",
    "soy_milk", "extra_shot",
    size="large", takeaway=True
))

# Negative test case raises a SyntaxError
#print(make_coffee(order_id=101, "latte", "Alice"))