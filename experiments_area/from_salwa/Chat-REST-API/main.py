import random

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
async def add_user(request: Request) -> dict:
    data = await request.json()
    missing = missing_field(data, ["name"])

    if missing:
        return {"error": f"Missing field: {missing}"}

    user = {"id": next_id(users), "name": data["name"]}
    users.append(user)

    return {"message": "User added successfully!", "user": user}


@app.get("/users")
async def get_users(user_id: int | None = None) -> dict:
    if user_id is not None:
        user = find_by_id(users, user_id)
        if user is None:
            return {"error": f"User {user_id} not found"}
        return {"users": [user], "count": 1}

    return {"users": users, "count": len(users)}


@app.post("/bots/add")
async def add_bot(request: Request) -> dict:
    data = await request.json()
    missing = missing_field(data, ["name"])

    if missing:
        return {"error": f"Missing field: {missing}"}

    bot = {"id": next_id(bots), "name": data["name"]}
    bots.append(bot)

    return {"message": "Bot added successfully!", "bot": bot}


@app.get("/bots")
async def get_bots(bot_id: int | None = None) -> dict:
    if bot_id is not None:
        bot = find_by_id(bots, bot_id)
        if bot is None:
            return {"error": f"Bot {bot_id} not found"}
        return {"bots": [bot], "count": 1}

    return {"bots": bots, "count": len(bots)}


@app.post("/conversations/start")
async def start_conversation(request: Request) -> dict:
    data = await request.json()
    missing = missing_field(data, ["user_id", "bot_id"])

    if missing:
        return {"error": f"Missing field: {missing}"}

    user = find_by_id(users, data["user_id"])
    if user is None:
        return {"error": f"User {data['user_id']} not found"}

    bot = find_by_id(bots, data["bot_id"])
    if bot is None:
        return {"error": f"Bot {data['bot_id']} not found"}

    conversation = {
        "id": next_id(conversations),
        "user_id": user["id"],
        "bot_id": bot["id"],
    }
    conversations.append(conversation)

    return {
        "message": "Conversation started!",
        "conversation": conversation,
    }


@app.get("/conversations")
async def get_conversations(user_id: int | None = None) -> dict:
    if user_id is None:
        result = conversations.copy()
    else:
        result = [c for c in conversations if c["user_id"] == user_id]

    return {"conversations": result, "count": len(result)}


@app.get("/conversations/show")
async def show_conversation(conversation_id: int) -> dict:
    conversation = find_by_id(conversations, conversation_id)

    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    conversation_messages = [
        m for m in messages if m["conversation_id"] == conversation_id
    ]

    return {
        "conversation": conversation,
        "messages": conversation_messages,
        "count": len(conversation_messages),
    }


@app.post("/messages/ask")
async def ask_question(request: Request) -> dict:
    data = await request.json()
    missing = missing_field(data, ["conversation_id", "text"])

    if missing:
        return {"error": f"Missing field: {missing}"}

    conversation = find_by_id(conversations, data["conversation_id"])

    if conversation is None:
        return {"error": f"Conversation {data['conversation_id']} not found"}

    chat_message = {
        "id": next_id(messages),
        "conversation_id": conversation["id"],
        "sender_type": "user",
        "sender_id": conversation["user_id"],
        "text": data["text"],
        "reply_to": None,
    }
    messages.append(chat_message)

    return {
        "message": "Query saved!",
        "chat_message": chat_message,
    }


@app.post("/messages/reply")
async def reply_to_question(request: Request) -> dict:
    data = await request.json()
    missing = missing_field(data, ["reply_to"])

    if missing:
        return {"error": f"Missing field: {missing}"}

    original = find_by_id(messages, data["reply_to"])

    if original is None or original["sender_type"] != "user":
        return {"error": f"User message {data['reply_to']} not found"}

    for message in messages:
        if message["reply_to"] == original["id"]:
            return {"error": f"Message {original['id']} already has a reply"}

    conversation = find_by_id(conversations, original["conversation_id"])

    if conversation is None:
        return {"error": f"Conversation {original['conversation_id']} not found"}

    chat_message = {
        "id": next_id(messages),
        "conversation_id": original["conversation_id"],
        "sender_type": "bot",
        "sender_id": conversation["bot_id"],
        "text": random.choice(bot_replies),
        "reply_to": original["id"],
    }
    messages.append(chat_message)

    return {
        "message": "Reply saved!",
        "chat_message": chat_message,
    }


@app.get("/messages")
async def get_messages(
    conversation_id: int | None = None,
    sender_type: str | None = None,
) -> dict:
    result = messages.copy()

    if conversation_id is not None:
        result = [m for m in result if m["conversation_id"] == conversation_id]

    if sender_type is not None:
        result = [m for m in result if m["sender_type"] == sender_type]

    return {"messages": result, "count": len(result)}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
