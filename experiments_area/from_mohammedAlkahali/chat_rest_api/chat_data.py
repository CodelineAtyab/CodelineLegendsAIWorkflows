users: list[dict] = [
    {"id": 1, "name": "Salim"},
    {"id": 2, "name": "Sara"}
]

bots: list[dict] = [
    {"id": 1, "name": "HelperBot"},
    {"id": 2, "name": "FunnyBot"}
]

messages: list[dict] = []

conversations: list[dict] = []

bot_replies: list[str] = [
    "That is a great question!",
    "Let me think about that... I would say yes.",
    "I am not sure, but you can check the documentation.",
    "Interesting! Can you tell me more?",
    "A Python web framework.",
    "Try restarting it, that fixes most things."
]


def find_by_id(items: list[dict], item_id: int) -> dict | None:
    """Return the item with this id, or None if it is not in the list."""
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def next_id(items: list[dict]) -> int:
    """Return one more than the highest id in the list, or 1 for an empty list."""
    highest_id = 0
    for item in items:
        if item["id"] > highest_id:
            highest_id = item["id"]
    return highest_id + 1


def find_missing_field(json_body: dict, required_fields: list[str]) -> str | None:
    """Return the name of the first required field that is missing, or None."""
    for field in required_fields:
        if json_body.get(field) is None:
            return field
    return None


def find_reply(message_id: int) -> dict | None:
    """Return the bot message that replies to this user message, or None."""
    for message in messages:
        if message["reply_to"] == message_id:
            return message
    return None
