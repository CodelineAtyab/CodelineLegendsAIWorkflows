orders: list[dict] = [
{"name": "Alice", "drink": "Latte", "size_oz": 16},
{"name": "mohammed", "drink": "ColdBrew", "size_oz": 20},
{"name": "Ahmed", "drink": "SpanishLatte", "size_oz": 15}]


def is_larger(order: dict) -> bool:
    return order["size_oz"] > 16

