# MakeCoffee

A tiny Python utility for representing a coffee order as a single, structured dictionary. The function keeps the API intentionally compact while still preserving the details that a barista or support tool needs: the order identifier, coffee type, customer name, optional add-ons, and order configuration.

## Why this design

The implementation uses a simple function signature:

```python
make_coffee(order_id, coffee_type, customer_name, *extras, **options)
```

This design keeps the required data explicit and linear while allowing flexible order customisation without introducing a larger validation layer or custom class hierarchy.

### Design decisions

- Required fields stay positional for clarity and easy reads in simple scripts.
- Optional extras are captured through `*extras` so toppings like `"soy_milk"` and `"extra_shot"` can be appended naturally.
- Named options like `size="large"` and `takeaway=True` are preserved in `**options`, which matches Python's standard argument pattern for configuration flags.
- The result is a plain dictionary so it is easy to serialize, print, log, or pass to a downstream API or database layer.

### Trade-offs

- The function prioritises flexibility over strict validation. This keeps the code short and approachable, but it does not enforce allowed coffee types, valid extras, or well-formed option names.
- Using a dictionary return value is easy to work with in Python, but it is intentionally not a full domain model or a formal schema. That keeps the project lightweight and suitable for a small example or prototype.
- The implementation avoids extra dependencies or abstraction layers, which makes it easy to understand and teach.

### Training references

This exercise is aligned with core Python concepts covered in beginner and intermediate training:

- Python function arguments: positional arguments, variadic arguments, and keyword arguments.
- `*args` and `**kwargs` patterns for flexible APIs.
- Working with tuples and dictionaries as structured data containers.
- Designing API surfaces that are simple to call while still scalable for small prototypes.

References and conceptual anchors:

- Python documentation: "Defining Functions" and argument-passing semantics.
- Python docs on `*args` and `**kwargs` usage patterns.
- Introductory Python training on data structures and API design.

## Example

```python
from coffee import make_coffee

order = make_coffee(
    101,
    "latte",
    "Alice",
    "soy_milk",
    "extra_shot",
    size="large",
    takeaway=True,
)

print(order)
```

This produces a single dictionary that captures the order in a compact, readable form.
