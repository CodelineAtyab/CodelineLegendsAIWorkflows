# Coffee Order Function

## About
This project practices Python functions using `*extras` and `**options`.

## How It Works
The `make_coffee` function requires:
- Order ID
- Coffee type
- Customer name

It returns a dictionary containing the order details.
Extra positional arguments are stored in a tuple.
Extra keyword arguments are stored in a dictionary.

Without extras or options, the function returns an empty tuple and dictionary.

## Example
```python
make_coffee(
    101, "latte", "Alice",
    "soy_milk", "extra_shot",
    size="large", takeaway=True
)
```

## Design and Trade-offs
- Extras and options are kept unchanged.
- New extras and options can be added without changing the function signature.
- Option names and values are not validated, so spelling mistakes are accepted.

## Tests
The tests check:
- An order without extras or options.
- An order with extras and options.
- A positional argument after a keyword argument raises SyntaxError.

Run the tests from this folder:
```bash
uv run python -m unittest -v
```

## Training References
- [Repository contribution guidelines](../../../README.md)
- Python function examples shared in Slack #material.