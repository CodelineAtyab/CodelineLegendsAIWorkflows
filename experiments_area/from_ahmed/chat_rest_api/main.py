from random import choice
import uvicorn
from fastapi import FastAPI, Request

from chat_data import (
    bot_replies,
    bots,
    conversations,
    filter_messages,
    find_by_id,
    get_missing_field,
    get_next_id,
    has_reply,
    messages,
    users,
)

app = FastAPI()


@app.post("/users/add")
async def add_user(request: Request) -> dict:
    """Add a new user with a unique ID."""
    body = await request.json()
    missing = get_missing_field(body, ("name",))
    if missing is not None:
        return {"error": f"Missing field: {missing}"}

    new_user = {"id": get_next_id(users), "name": body["name"]}
    users.append(new_user)
    return {"message": "User added successfully!", "user": new_user}


@app.get("/users")
async def get_users(user_id: int | None = None) -> dict:
    """List all users or fetch a specific user by ID."""
    if user_id is None:
        return {"users": users, "count": len(users)}

    user = find_by_id(users, user_id)
    if user is None:
        return {"error": f"User {user_id} not found"}
    return {"user": user}


@app.post("/bots/add")
async def add_bot(request: Request) -> dict:
    """Add a new bot with a unique ID."""
    body = await request.json()
    missing = get_missing_field(body, ("name",))
    if missing is not None:
        return {"error": f"Missing field: {missing}"}

    new_bot = {"id": get_next_id(bots), "name": body["name"]}
    bots.append(new_bot)
    return {"message": "Bot added successfully!", "bot": new_bot}


@app.get("/bots")
async def get_bots(bot_id: int | None = None) -> dict:
    """List all bots or fetch a specific bot by ID."""
    if bot_id is None:
        return {"bots": bots, "count": len(bots)}

    bot = find_by_id(bots, bot_id)
    if bot is None:
        return {"error": f"Bot {bot_id} not found"}
    return {"bot": bot}


@app.post("/conversations/start")
async def start_conversation(request: Request) -> dict:
    """Initiate a conversation between an existing user and bot."""
    body = await request.json()
    missing = get_missing_field(body, ("user_id", "bot_id"))
    if missing is not None:
        return {"error": f"Missing field: {missing}"}

    user_id = body["user_id"]
    bot_id = body["bot_id"]

    if find_by_id(users, user_id) is None:
        return {"error": f"User {user_id} not found"}
    if find_by_id(bots, bot_id) is None:
        return {"error": f"Bot {bot_id} not found"}

    conv = {
        "id": get_next_id(conversations),
        "user_id": user_id,
        "bot_id": bot_id,
    }
    conversations.append(conv)
    return {"message": "Conversation started!", "conversation": conv}


@app.get("/conversations")
async def get_conversations(user_id: int | None = None) -> dict:
    """List conversations, optionally filtered by user ID."""
    filtered = [
        conv for conv in conversations
        if user_id is None or conv["user_id"] == user_id
    ]
    return {"conversations": filtered, "count": len(filtered)}


@app.get("/conversations/show")
async def show_conversation(conversation_id: int) -> dict:
    """Display conversation metadata and messages in creation order."""
    conv = find_by_id(conversations, conversation_id)
    if conv is None:
        return {"error": f"Conversation {conversation_id} not found"}

    conv_messages = filter_messages(conversation_id=conversation_id)
    return {
        "conversation": conv,
        "messages": conv_messages,
        "count": len(conv_messages),
    }


@app.post("/messages/ask")
async def ask_message(request: Request) -> dict:
    """Post a user query to an active conversation."""
    body = await request.json()
    missing = get_missing_field(body, ("conversation_id", "text"))
    if missing is not None:
        return {"error": f"Missing field: {missing}"}

    conv_id = body["conversation_id"]
    conv = find_by_id(conversations, conv_id)
    if conv is None:
        return {"error": f"Conversation {conv_id} not found"}

    msg = {
        "id": get_next_id(messages),
        "conversation_id": conv_id,
        "sender_type": "user",
        "sender_id": conv["user_id"],
        "text": body["text"],
        "reply_to": None,
    }
    messages.append(msg)
    return {"message": "Query saved!", "chat_message": msg}


@app.post("/messages/reply")
async def reply_message(request: Request) -> dict:
    """Generate a canned bot reply for an unanswered user query."""
    body = await request.json()
    missing = get_missing_field(body, ("reply_to",))
    if missing is not None:
        return {"error": f"Missing field: {missing}"}

    reply_to = body["reply_to"]
    query_msg = find_by_id(messages, reply_to)

    if query_msg is None or query_msg["sender_type"] != "user":
        return {"error": f"User message {reply_to} not found"}

    if has_reply(reply_to):
        return {"error": f"Message {reply_to} already has a reply"}

    conv = find_by_id(conversations, query_msg["conversation_id"])
    if conv is None:
        return {"error": f"Conversation {query_msg['conversation_id']} not found"}

    reply_msg = {
        "id": get_next_id(messages),
        "conversation_id": conv["id"],
        "sender_type": "bot",
        "sender_id": conv["bot_id"],
        "text": choice(bot_replies),
        "reply_to": reply_to,
    }
    messages.append(reply_msg)
    return {"message": "Reply saved!", "chat_message": reply_msg}


@app.get("/messages")
async def get_messages(
    conversation_id: int | None = None,
    sender_type: str | None = None,
) -> dict:
    """Retrieve messages with optional filters in chronological order."""
    filtered = filter_messages(conversation_id, sender_type)
    return {"messages": filtered, "count": len(filtered)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
