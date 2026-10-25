from typing import Any

users: list[dict[str, Any]] = [
    {"id": 1, "name": "Salim"},
    {"id": 2, "name": "Sara"},
]

bots: list[dict[str, Any]] = [
    {"id": 1, "name": "HelperBot"},
    {"id": 2, "name": "StudyBot"},
]

messages: list[dict[str, Any]] = []
conversations: list[dict[str, Any]] = []

bot_replies: list[str] = [
    "That is a great question.",
    "Here is a helpful way to think about it.",
    "FastAPI makes building APIs with Python straightforward.",
    "Let us break that down step by step.",
    "I can help you explore that topic.",
]


def find_by_id(items: list[dict[str, Any]], item_id: int) -> dict[str, Any] | None:
    """Find and return an item by its id."""
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def next_id(items: list[dict[str, Any]]) -> int:
    """Return one more than the highest id in a list."""
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


def missing_field(body: dict[str, Any], fields: list[str]) -> str | None:
    """Return the first required field missing from a request body."""
    for field in fields:
        if body.get(field) is None:
            return field
    return None
