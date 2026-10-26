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
    "Thanks for reaching out!",
    "Could you provide more context on that?",
    "That is an interesting topic to explore.",
    "Let us break this down step by step.",
    "Try running a small test to verify the behavior.",
]


def find_by_id(items: list[dict], item_id: int) -> dict | None:
    """Return item matching given ID or None."""
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def get_next_id(items: list[dict]) -> int:
    """Generate next incremental ID for resource."""
    return max((item["id"] for item in items), default=0) + 1


def get_missing_field(body: dict, required_fields: tuple[str, ...]) -> str | None:
    """Check for missing required payload keys."""
    for field in required_fields:
        if body.get(field) is None:
            return field
    return None


def has_reply(message_id: int) -> bool:
    """Check if user message already has an associated bot reply."""
    for msg in messages:
        if msg["sender_type"] == "bot" and msg["reply_to"] == message_id:
            return True
    return False


def filter_messages(
    conversation_id: int | None = None,
    sender_type: str | None = None,
) -> list[dict]:
    """Return messages filtered by conversation or sender type in creation order."""
    filtered = []
    for msg in messages:
        if conversation_id is not None and msg["conversation_id"] != conversation_id:
            continue
        if sender_type is not None and msg["sender_type"] != sender_type:
            continue
        filtered.append(msg)
    return filtered
