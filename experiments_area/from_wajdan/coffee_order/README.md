# Coffee Order Function

## About
A simple Python function that returns coffee order details.

## Function
```python
make_coffee(order_id, coffee_type, customer_name, *extras, **options)
```

- `order_id`: the order number.
- `coffee_type`: the type of coffee.
- `customer_name`: the customer's name.
- `extras`: extra positional arguments stored in a tuple.
- `options`: extra keyword arguments stored in a dictionary.

## Example
```python
from coffee import make_coffee

order = make_coffee(
    101, "espresso", "Wajdan",
    "soy_milk", "extra_shot",
    size="large", takeaway=True
)

print(order)
```

Result:
```python
{
    "order_id": 101,
    "coffee_type": "espresso",
    "customer_name": "Wajdan",
    "extras": ("soy_milk", "extra_shot"),
    "options": {"size": "large", "takeaway": True}
}
```

## Design and Trade-offs
The function keeps extras and options unchanged.
Without them, it returns an empty tuple and dictionary.

Using `*extras` and `**options` allows new additions without changing the signature.
However, option names and values are not validated, so misspelled options are accepted.

## Tests
The tests use Python's built-in `unittest` library to check:
- An order without extras or options.
- An order with extras and options.
- An invalid argument order that raises `SyntaxError`.

Run from the project folder:
```bash
uv run python -m unittest -v
```
