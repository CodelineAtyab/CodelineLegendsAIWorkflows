users = [
    {"id": 1, "name": "Salim"},
    {"id": 2, "name": "Sara"},
]

bots = [
    {"id": 1, "name": "HelperBot"},
    {"id": 2, "name": "StudyBot"},
]

messages = []
conversations = []

bot_replies: list[str] = [
    "Hello! How can I help you?",
    "FastAPI is a Python web framework.",
    "Let me explain that step by step.",
    "That is a great question!",
    "Please provide more details.",
]


def find_by_id(items: list[dict], item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def next_id(items: list[dict]) -> int:
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


def missing_field(data: dict, fields: list[str]):
    for field in fields:
        if field not in data or data[field] is None:
            return field
    return None
