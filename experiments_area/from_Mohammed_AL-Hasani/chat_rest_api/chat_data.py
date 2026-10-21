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
    "A Python web framework.",
    "You can use a decorator to define a FastAPI route.",
    "A query parameter is passed in the URL.",
    "A JSON body contains data sent with a request.",
    "FastAPI can return Python dictionaries as JSON.",
    "You can use POST to create a new resource.",
]


def find_by_id(items: list[dict], item_id: int) -> dict | None:
    for item in items:
        if item["id"] == item_id:
            return item

    return None


def create_next_id(items: list[dict]) -> int:
    if not items:
        return 1

    return max(item["id"] for item in items) + 1


def get_missing_field(
    body: dict,
    required_fields: list[str],
) -> str | None:
    if not isinstance(body, dict):
        return required_fields[0]

    for field in required_fields:
        if body.get(field) is None:
            return field

    return None
