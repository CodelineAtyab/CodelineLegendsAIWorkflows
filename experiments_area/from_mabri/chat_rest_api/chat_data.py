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
        if item["id"] > highest:
            highest = item["id"]
    return highest + 1


def missing_field(body: dict, fields: list[str]) -> str | None:
    for field in fields:
        if body.get(field) is None:
            return field
    return None
