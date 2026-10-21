users: list[dict] = [
    {"id": 1, "name": "Salim"},
    {"id": 2, "name": "Sara"},
]

bots: list[dict] = [
    {"id": 1, "name": "HelperBot"},
    {"id": 2, "name": "StudyBot"},
]

messages: list[dict] = []
conversations: list[dict] = []

bot_replies: list[str] = [
    "Thanks for your question.",
    "Could you explain that in more detail?",
    "That is an interesting question.",
    "Let us think about it step by step.",
    "Try a small example to understand it better.",
]


def find_by_id(items: list[dict], item_id: int) -> dict | None:
    """Return the item with the given ID, or None when it does not exist."""
    for item in items:
        if item["id"] == item_id:
            return item

    return None


def get_next_id(items: list[dict]) -> int:
    """Return one more than the highest ID, or 1 for an empty list."""
    return max((item["id"] for item in items), default=0) + 1


def get_missing_field(body: dict, required_fields: tuple[str, ...]) -> str | None:
    """Return the first missing field name, or None when all are supplied."""
    for field in required_fields:
        if body.get(field) is None:
            return field

    return None


def has_reply(message_id: int) -> bool:
    """Check whether a user message already has a bot reply."""
    for message in messages:
        if message["sender_type"] == "bot" and message["reply_to"] == message_id:
            return True

    return False


def filter_messages(
    conversation_id: int | None = None,
    sender_type: str | None = None,
) -> list[dict]:
    """Return matching messages in their original creation order."""
    result = []

    for message in messages:
        if conversation_id is not None and message["conversation_id"] != conversation_id:
            continue

        if sender_type is not None and message["sender_type"] != sender_type:
            continue

        result.append(message)

    return result