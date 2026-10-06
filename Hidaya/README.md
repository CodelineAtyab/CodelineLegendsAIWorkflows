# Coffee Order Function

## Purpose
The make_coffee function stores a coffee order in a dictionary.

## Parameters
- order_id: required order number.
- coffee_type: required coffee name.
- customer_name: required customer name.
- *extras: additional positional arguments stored in a tuple.
- **options: additional keyword arguments stored in a dictionary.

## Example
```python
make_coffee(
    101, "latte", "Alice", "soy_milk", "extra_shot", size="large", takeaway=True
)
```

## Design Decisions
The first three parameters are required.
Extras and options are returned unchanged.
Without extras or options, the function returns an empty tuple
and an empty dictionary.

## Benefits
- Accepts any number of extras and options.
- New extras and options do not require changing the function.
- Existing calls with only three arguments still work.

## Trade-offs
- Misspelled option names are accepted.
- Extra values are not validated.
- Supported options are less obvious than explicit parameters.

## Tests
Tests check:
1. An order with only the required arguments.
2. An order containing extras and options.
3. A SyntaxError when an ordinary positional argument follows
   a keyword argument.

Run the tests:
```bash
python -m unittest -v
```

## Training References
Refer to the sample Git files shared during training.
Their exact filenames and repository links were not provided.
Add those references here when available.