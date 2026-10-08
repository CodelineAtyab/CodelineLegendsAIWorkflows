
# Coffee Order Function

## Description
This project creates coffee orders using Python.

## Arguments
- order_id, coffee_type, customer_name are required.
- *extras stores extra items in a tuple.
- **options stores additional settings in a dictionary.

## Trade-offs

Advantages:
- *extras lets us add many extra items.
- **options lets us add different settings.
- We don't need to change the function every time.

Disadvantages:
- Users can enter wrong option names.
- The function does not check if the values are correct.

## Tests
1. Coffee without extras and options.
2. Coffee with extras and options.
3. Invalid argument order (commented out because it causes a SyntaxError).

## Training Reference
I learned about functions, positional arguments,
keyword arguments, *args and **kwargs in Codeline training.

Training file: [Enter the actual training filename here]
