users: list[dict] = [
    {"id": 1, "name": "Salim"},
    {"id": 2, "name": "Maryam"},
]

bots: list[dict] = [
    {"id": 1, "name": "HelperBot"},
    {"id": 2, "name": "QuizBot"},
]

conversations: list[dict] = []

messages: list[dict] = []

bot_replies: list[str] = [
    "A Python web framework.",
    "Good question! Let me think about it.",
    "You can find more details in the documentation.",
    "That is a great topic to practise.",
    "Try it step by step and see what happens.",
]


def find_by_id(items: list[dict], item_id: int) -> dict | None:
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def get_next_id(items: list[dict]) -> int:
    highest_id = 0
    for item in items:
        highest_id = max(highest_id, item["id"])
    return highest_id + 1


def find_missing_field(json_body: dict, required_fields: list[str]) -> str | None:
    for field in required_fields:
        if json_body.get(field) is None:
            return field
    return None


def has_reply(items: list[dict], message_id: int) -> bool:
    for item in items:
        if item["reply_to"] == message_id:
            return True
    return False
