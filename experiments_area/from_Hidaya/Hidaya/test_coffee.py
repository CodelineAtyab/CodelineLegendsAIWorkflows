from coffee import make_coffee

order = make_coffee(
    101, "latte", "Alice",
    "soy_milk", "extra_shot",
    size="large", takeaway=True,
)

print(order)
