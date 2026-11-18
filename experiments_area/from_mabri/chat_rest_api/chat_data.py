users: list[dict] = [
    {"id": 1, "name": "Salim"},
    {"id": 2, "name": "Sara"},
]

bots: list[dict] = [
    {"id": 1, "name": "HelperBot"},
    {"id": 2, "name": "JokeBot"},
]

messages: list[dict] = []

conversations: list[dict] = []

bot_replies: list[str] = [
    "That is a great question!",
    "Let me think... the answer is 42.",
    "I am not sure, but I will learn it soon.",
    "Have you tried turning it off and on again?",
    "Good point! Tell me more.",
]


def find_by_id(items: list[dict], item_id: int) -> dict | None:
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def next_id(items: list[dict]) -> int:
    highest = 0
    for item in items:
        highest = max(highest, item["id"])
    return highest + 1


def check_fields(body: dict, fields: dict[str, type]) -> str | None:
    # Returns an error message for the first bad field, or None if all are fine.
    # type(...) is used instead of isinstance so that true/false don't count
    # as ints (in Python, True == 1).
    for field, expected_type in fields.items():
        value = body.get(field)
        if value is None or value == "":
            return f"Missing field: {field}"
        if type(value) is not expected_type:
            return f"Invalid field: {field} must be {expected_type.__name__}"
    return None
