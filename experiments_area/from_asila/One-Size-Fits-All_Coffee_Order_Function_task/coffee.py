def main():
    print("Hello from one-size-fits-all-coffee-order-function-task!")


if __name__ == "__main__":
    main()


def make_coffee(order_id, coffee_type, customer_name, *extras, **options):
    return {
        "order_id": order_id,
        "coffee_type": coffee_type,
        "customer_name": customer_name,
        "extras": extras,
        "options": options,
    }


order = make_coffee(
    112, "matcha", "Asila", "oat_milk", "vanilla", size="medium", takeaway=True
)

print(order)
