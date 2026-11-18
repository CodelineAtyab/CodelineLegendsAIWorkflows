import random

import uvicorn
from fastapi import FastAPI, Request

from chat_data import (
    bot_replies,
    bots,
    conversations,
    create_next_id,
    find_by_id,
    get_missing_field,
    messages,
    users,
)

app = FastAPI()


@app.post("/users/add")
async def add_user(request: Request) -> dict:
    body = await request.json()

    missing_field = get_missing_field(body, ["name"])
    if missing_field:
        return {"error": f"Missing field: {missing_field}"}

    new_user = {
        "id": create_next_id(users),
        "name": body["name"],
    }

    users.append(new_user)

    return {
        "message": "User added successfully!",
        "user": new_user,
    }


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
    body = await request.json()

    missing_field = get_missing_field(body, ["name"])
    if missing_field:
        return {"error": f"Missing field: {missing_field}"}

    new_bot = {
        "id": create_next_id(bots),
        "name": body["name"],
    }

    bots.append(new_bot)

    return {
        "message": "Bot added successfully!",
        "bot": new_bot,
    }


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
    body = await request.json()

    missing_field = get_missing_field(
        body,
        ["user_id", "bot_id"],
    )
    if missing_field:
        return {"error": f"Missing field: {missing_field}"}

    user_id = body["user_id"]
    bot_id = body["bot_id"]

    user = find_by_id(users, user_id)
    if user is None:
        return {"error": f"User {user_id} not found"}

    bot = find_by_id(bots, bot_id)
    if bot is None:
        return {"error": f"Bot {bot_id} not found"}

    new_conversation = {
        "id": create_next_id(conversations),
        "user_id": user_id,
        "bot_id": bot_id,
    }

    conversations.append(new_conversation)

    return {
        "message": "Conversation started!",
        "conversation": new_conversation,
    }


@app.get("/conversations")
async def get_conversations(
    user_id: int | None = None,
) -> dict:
    result = []

    for conversation in conversations:
        if user_id is None or conversation["user_id"] == user_id:
            result.append(conversation)

    return {
        "conversations": result,
        "count": len(result),
    }


@app.get("/conversations/show")
async def show_conversation(
    conversation_id: int,
) -> dict:
    conversation = find_by_id(conversations, conversation_id)

    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    conversation_messages = []

    for chat_message in messages:
        if chat_message["conversation_id"] == conversation_id:
            conversation_messages.append(chat_message)

    return {
        "conversation": conversation,
        "messages": conversation_messages,
        "count": len(conversation_messages),
    }


@app.post("/messages/ask")
async def ask_question(request: Request) -> dict:
    body = await request.json()

    missing_field = get_missing_field(
        body,
        ["conversation_id", "text"],
    )
    if missing_field:
        return {"error": f"Missing field: {missing_field}"}

    conversation_id = body["conversation_id"]
    conversation = find_by_id(conversations, conversation_id)

    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    new_message = {
        "id": create_next_id(messages),
        "conversation_id": conversation_id,
        "sender_type": "user",
        "sender_id": conversation["user_id"],
        "text": body["text"],
        "reply_to": None,
    }

    messages.append(new_message)

    return {
        "message": "Query saved!",
        "chat_message": new_message,
    }


@app.post("/messages/reply")
async def reply_to_question(request: Request) -> dict:
    body = await request.json()

    missing_field = get_missing_field(body, ["reply_to"])
    if missing_field:
        return {"error": f"Missing field: {missing_field}"}

    reply_to = body["reply_to"]
    question = find_by_id(messages, reply_to)

    if question is None or question["sender_type"] != "user":
        return {"error": f"User message {reply_to} not found"}

    for chat_message in messages:
        if chat_message["reply_to"] == reply_to:
            return {"error": f"Message {reply_to} already has a reply"}

    conversation = find_by_id(
        conversations,
        question["conversation_id"],
    )

    if conversation is None:
        return {"error": (f"Conversation {question['conversation_id']} not found")}

    new_message = {
        "id": create_next_id(messages),
        "conversation_id": question["conversation_id"],
        "sender_type": "bot",
        "sender_id": conversation["bot_id"],
        "text": random.choice(bot_replies),
        "reply_to": reply_to,
    }

    messages.append(new_message)

    return {
        "message": "Reply saved!",
        "chat_message": new_message,
    }


@app.get("/messages")
async def get_messages(
    conversation_id: int | None = None,
    sender_type: str | None = None,
) -> dict:
    result = []

    for chat_message in messages:
        if (
            conversation_id is not None
            and chat_message["conversation_id"] != conversation_id
        ):
            continue

        if sender_type is not None and chat_message["sender_type"] != sender_type:
            continue

        result.append(chat_message)

    return {
        "messages": result,
        "count": len(result),
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
