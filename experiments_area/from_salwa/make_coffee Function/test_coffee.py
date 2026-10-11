def make_coffee( order_id, coffee_type, customer_name,*extras,**options):
    
    return {

"order_id": order_id,
"coffee_type":coffee_type,
"customer_name":customer_name,
"extras":extras,
"options":options
}

result =make_coffee(
    101, "latte", "Alice",
    "soy_milk", "extra_shot",
    size="large", takeaway=True
)

print(result)


def test_make_coffee():
    result = make_coffee(
        101,
        "latte",
        "Alice"
    )

    expected = {
        "order_id": 101,
        "coffee_type": "latte",
        "customer_name": "Alice",
        "extras": (),
        "options": {}
    }

    if result==expected:
        print("pass")
    else:
        print("fail")
    return result


test_make_coffee()