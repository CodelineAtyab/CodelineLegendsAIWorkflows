users: list[dict] = [
    {"id": 1, "name": "Sara"},
    {"id": 2, "name": "Ahmed"},
]

bots: list[dict] = [
    {"id": 1, "name": "HelperBot"},
    {"id": 2, "name": "QuizBot"},
]

messages: list[dict] = []

conversations: list[dict] = []

bot_replies: list[str] = [
    "A Python web framework.",
    "That is a great question!",
    "Let me think about it... the answer is 42.",
    "I am not sure, please ask me again later.",
    "Try reading the docs, they explain it well.",
]


def find_by_id(items: list[dict], item_id: int) -> dict | None:
    for item in items:
        if item["id"] == item_id:
            return item
    return None


# A new id is one more than the highest id in the list, or 1 for an empty list
def next_id(items: list[dict]) -> int:
    if len(items) == 0:
        return 1
    return max(item["id"] for item in items) + 1


# Returns the name of the first required field missing from the body, or None
def find_missing_field(json_body: dict, required_fields: list[str]) -> str | None:
    for field in required_fields:
        if json_body.get(field) is None:
            return field
    return None
