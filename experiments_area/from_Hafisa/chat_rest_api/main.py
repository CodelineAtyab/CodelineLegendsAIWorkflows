from random import choice
from typing import Any

import uvicorn
from fastapi import FastAPI, Request

from chat_data import (
    bot_replies,
    bots,
    conversations,
    find_by_id,
    messages,
    missing_field,
    next_id,
    users,
)

app = FastAPI()


@app.post("/users/add")
async def add_user(request: Request) -> dict[str, Any]:
    """Add a user to the in-memory users list."""
    body = await request.json()
    missing = missing_field(body, ["name"])
    if missing:
        return {"error": f"Missing field: {missing}"}

    user = {"id": next_id(users), "name": body["name"]}
    users.append(user)
    return {"message": "User added successfully!", "user": user}


@app.get("/users")
async def get_users(user_id: int | None = None) -> dict[str, Any]:
    """Return all users or one user by id."""
    if user_id is None:
        return {"users": users, "count": len(users)}

    user = find_by_id(users, user_id)
    if user is None:
        return {"error": f"User {user_id} not found"}
    return {"users": [user], "count": 1}


@app.post("/bots/add")
async def add_bot(request: Request) -> dict[str, Any]:
    """Add a bot to the in-memory bots list."""
    body = await request.json()
    missing = missing_field(body, ["name"])
    if missing:
        return {"error": f"Missing field: {missing}"}

    bot = {"id": next_id(bots), "name": body["name"]}
    bots.append(bot)
    return {"message": "Bot added successfully!", "bot": bot}


@app.get("/bots")
async def get_bots(bot_id: int | None = None) -> dict[str, Any]:
    """Return all bots or one bot by id."""
    if bot_id is None:
        return {"bots": bots, "count": len(bots)}

    bot = find_by_id(bots, bot_id)
    if bot is None:
        return {"error": f"Bot {bot_id} not found"}
    return {"bots": [bot], "count": 1}


@app.post("/conversations/start")
async def start_conversation(request: Request) -> dict[str, Any]:
    """Start a conversation between an existing user and bot."""
    body = await request.json()
    missing = missing_field(body, ["user_id", "bot_id"])
    if missing:
        return {"error": f"Missing field: {missing}"}

    user = find_by_id(users, body["user_id"])
    if user is None:
        return {"error": f"User {body['user_id']} not found"}

    bot = find_by_id(bots, body["bot_id"])
    if bot is None:
        return {"error": f"Bot {body['bot_id']} not found"}

    conversation = {
        "id": next_id(conversations),
        "user_id": user["id"],
        "bot_id": bot["id"],
    }
    conversations.append(conversation)
    return {"message": "Conversation started!", "conversation": conversation}


@app.get("/conversations")
async def get_conversations(user_id: int | None = None) -> dict[str, Any]:
    """Return all conversations or those belonging to one user."""
    results = conversations
    if user_id is not None:
        results = [
            conversation
            for conversation in conversations
            if conversation["user_id"] == user_id
        ]
    return {"conversations": results, "count": len(results)}


@app.get("/conversations/show")
async def show_conversation(conversation_id: int) -> dict[str, Any]:
    """Return a conversation and its messages in creation order."""
    conversation = find_by_id(conversations, conversation_id)
    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    conversation_messages = [
        message for message in messages if message["conversation_id"] == conversation_id
    ]
    return {
        "conversation": conversation,
        "messages": conversation_messages,
        "count": len(conversation_messages),
    }


@app.post("/messages/ask")
async def ask_message(request: Request) -> dict[str, Any]:
    """Save a user query in an existing conversation."""
    body = await request.json()
    missing = missing_field(body, ["conversation_id", "text"])
    if missing:
        return {"error": f"Missing field: {missing}"}

    conversation = find_by_id(conversations, body["conversation_id"])
    if conversation is None:
        return {"error": f"Conversation {body['conversation_id']} not found"}

    chat_message = {
        "id": next_id(messages),
        "conversation_id": conversation["id"],
        "sender_type": "user",
        "sender_id": conversation["user_id"],
        "text": body["text"],
        "reply_to": None,
    }
    messages.append(chat_message)
    return {"message": "Query saved!", "chat_message": chat_message}


@app.post("/messages/reply")
async def reply_to_message(request: Request) -> dict[str, Any]:
    """Save a canned bot reply to one user query."""
    body = await request.json()
    missing = missing_field(body, ["reply_to"])
    if missing:
        return {"error": f"Missing field: {missing}"}

    user_message = next(
        (
            message
            for message in messages
            if message["id"] == body["reply_to"] and message["sender_type"] == "user"
        ),
        None,
    )
    if user_message is None:
        return {"error": f"User message {body['reply_to']} not found"}

    if any(message["reply_to"] == user_message["id"] for message in messages):
        return {"error": f"Message {user_message['id']} already has a reply"}

    conversation = find_by_id(conversations, user_message["conversation_id"])
    chat_message = {
        "id": next_id(messages),
        "conversation_id": user_message["conversation_id"],
        "sender_type": "bot",
        "sender_id": conversation["bot_id"],
        "text": choice(bot_replies),
        "reply_to": user_message["id"],
    }
    messages.append(chat_message)
    return {"message": "Reply saved!", "chat_message": chat_message}


@app.get("/messages")
async def get_messages(
    conversation_id: int | None = None,
    sender_type: str | None = None,
) -> dict[str, Any]:
    """Return messages filtered by conversation and sender type."""
    results = messages
    if conversation_id is not None:
        results = [
            message
            for message in results
            if message["conversation_id"] == conversation_id
        ]
    if sender_type is not None:
        results = [
            message for message in results if message["sender_type"] == sender_type
        ]
    return {"messages": results, "count": len(results)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
