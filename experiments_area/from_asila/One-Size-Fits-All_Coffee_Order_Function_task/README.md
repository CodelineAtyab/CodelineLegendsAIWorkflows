Flexible make_coffee Function:

This project contains a flexible make_coffee function for creating coffee
orders with required information, optional extras, and additional options.

Files:

- coffee.py contains the make_coffee function.
- test_coffee.py checks the function using simple if/else statements.

Function signature:

make_coffee(order_id, coffee_type, customer_name, *extras, **options)
- order_id, coffee_type, and customer_name are mandatory.
- *extras collects extra positional values in an ordered tuple.
- **options collects extra keyword values in a dictionary.

Example:
from coffee import make_coffee

make_coffee(
    112,
    "matcha",
    "Asila",
    "oat_milk",
    "vanilla",
    size="medium",
    takeaway=True
)

Design decisions and trade-offs:

I used *extras and **options because customers can add different coffee
choices without changing the function every time a new choice is introduced.
Calls that provide only the three required values continue to work.
This pattern makes the function flexible, but it does not clearly show every
allowed extra or option in the function signature. A misspelled option can also
be accepted unless validation is added.
Python requires positional arguments to come before keyword arguments. An
invalid expression is kept as a comment in test_coffee.py:

# make_coffee(order_id=100, "matcha", "Asila")
