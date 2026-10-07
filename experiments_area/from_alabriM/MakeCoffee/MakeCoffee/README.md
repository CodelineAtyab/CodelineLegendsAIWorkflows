# MakeCoffee

A small practice function that takes a coffee order and returns it as one dictionary.

```python
make_coffee(order_id, coffee_type, customer_name, *extras, **options)
```

## What `*extras` and `**options` do

The first three parameters are normal and required: `order_id`, `coffee_type` and
`customer_name`.

`*extras` collects any leftover positional arguments into a tuple. If I pass
`"soy_milk", "extra_shot"`, then `extras` becomes `("soy_milk", "extra_shot")`. I can pass none,
one, or many.

`**options` collects any leftover keyword arguments into a dictionary. So `size="large",
takeaway=True` becomes `{"size": "large", "takeaway": True}`.

## One pro and one con

**Pro:** I can add new extras or options without changing the function. A customer can ask for
two add-ons or five, and it still works.

**Con:** Nothing is checked. If I spell an option wrong, like `siz="large"`, Python just puts it
into `options` and no error appears, so I only notice the mistake later.

## Where I learnt it

From `experiments_area/from_atyab/func_practice/function_with_flexible_parameters.py`, the
`get_branch_info_with_fixed_and_dynamic_params(commit_id, name, owner_name, *args, **kwargs)`
example. It has the same shape as mine: fixed parameters first, then `*args` and `**kwargs`.

## Example

```python
from coffee import make_coffee

order = make_coffee(101, "latte", "Alice", "soy_milk", "extra_shot", size="large", takeaway=True)
print(order)
```

Output:

```python
{'order_id': 101, 'coffee_type': 'latte', 'customer_name': 'Alice',
 'extras': ('soy_milk', 'extra_shot'), 'options': {'size': 'large', 'takeaway': True}}
```
