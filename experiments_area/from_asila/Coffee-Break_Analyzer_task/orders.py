def main():
    print("Hello from coffee-break-analyzer-task!")


if __name__ == "__main__":
    main()

#list dictionary
orders: list[dict] = [{"name": "ALex" , "drink":"latte" , "size_oz":16} ]


def is_large(order:dict) -> bool:
    return order[size_oz] >= 16