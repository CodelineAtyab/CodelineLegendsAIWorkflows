from random import randint

# Sample users
users: list[dict] = [
    {"id": 1, "name": "Baraah"},
    {"id": 2, "name": "Sara"},
]

# Sample bots
bots: list[dict] = [
    {"id": 1, "name": "HelperBot"},
    {"id": 2, "name": "StudyBot"},
]

# Empty lists for messages and conversations
messages: list[dict] = []
conversations: list[dict] = []

# Bot replies
bot_replies: list[str] = [
    "Hello! How can I help you?",
    "That is a good question!",
    "I am happy to help you.",
    "Can you explain your question?",
    "Thank you for asking!",
]


# Find an item by its ID
def find_by_id(items: list[dict], item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item

    return None


# Generate the next unique ID
def next_id(items: list[dict]) -> int:
    highest_id = 0

    for item in items:
        highest_id = max(highest_id, item["id"])

    return highest_id + 1


# Check for missing fields
def missing_field(body: dict, fields: list):
    for field in fields:
        if body.get(field) is None or body.get(field) == "":
            return field

    return None


# Pick a random bot reply
def get_bot_reply() -> str:
    random_number = randint(0, len(bot_replies) - 1)
    return bot_replies[random_number]
