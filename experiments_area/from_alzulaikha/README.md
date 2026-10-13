# Coffee Order Practice

This practice demonstrates how to use `*args` and `**kwargs` in Python to create a flexible `make_coffee` function.

## `*args`

`*args` allows the function to accept any number of additional positional arguments.

In this practice, `*extras` is used to store additional coffee extras such as `soy_milk` and `extra_shot`.

The values are stored as a tuple.

## `**kwargs`

`**kwargs` allows the function to accept any number of additional keyword arguments.

In this practice, `**options` is used to store options such as `size="large"` and `takeaway=True`.

The values are stored as a dictionary.

## Pros

- Makes the function flexible.
- Allows additional arguments without changing the function definition.
- Easy to extend with new coffee extras and options.

## Cons

- The function does not clearly specify all possible arguments.
- It can be harder to understand and validate the expected inputs.

## Training Reference

This practice follows the Python training examples and exercises covering flexible function arguments using `*args` and `**kwargs`.