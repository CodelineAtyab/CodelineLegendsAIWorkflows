from random import choice

import uvicorn
from fastapi import FastAPI, Request

from chat_data import (
    bot_replies,
    bots,
    conversations,
    find_by_id,
    find_missing_field,
    get_next_id,
    has_reply,
    messages,
    users,
)

app = FastAPI()


@app.get("/users")
async def view_users(user_id: int | None = None) -> dict:
    if user_id is None:
        return {"users": users, "count": len(users)}
    user = find_by_id(users, user_id)
    if user is None:
        return {"error": f"User {user_id} not found"}
    return {"user": user}


@app.post("/users/add")
async def add_user(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    missing = find_missing_field(json_body, ["name"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}

    new_user = {"id": get_next_id(users), "name": json_body["name"]}
    users.append(new_user)
    return {"message": "User added successfully!", "user": new_user}


@app.get("/bots")
async def view_bots(bot_id: int | None = None) -> dict:
    if bot_id is None:
        return {"bots": bots, "count": len(bots)}
    bot = find_by_id(bots, bot_id)
    if bot is None:
        return {"error": f"Bot {bot_id} not found"}
    return {"bot": bot}


@app.post("/bots/add")
async def add_bot(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    missing = find_missing_field(json_body, ["name"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}

    new_bot = {"id": get_next_id(bots), "name": json_body["name"]}
    bots.append(new_bot)
    return {"message": "Bot added successfully!", "bot": new_bot}


@app.post("/conversations/start")
async def start_conversation(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    missing = find_missing_field(json_body, ["user_id", "bot_id"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}

    user_id = json_body["user_id"]
    bot_id = json_body["bot_id"]

    if find_by_id(users, user_id) is None:
        return {"error": f"User {user_id} not found"}
    if find_by_id(bots, bot_id) is None:
        return {"error": f"Bot {bot_id} not found"}

    new_conversation = {
        "id": get_next_id(conversations),
        "user_id": user_id,
        "bot_id": bot_id,
    }
    conversations.append(new_conversation)
    return {"message": "Conversation started!", "conversation": new_conversation}


@app.get("/conversations")
async def view_conversations(user_id: int | None = None) -> dict:
    results = []
    for conversation in conversations:
        if user_id is not None and conversation["user_id"] != user_id:
            continue
        results.append(conversation)
    return {"conversations": results, "count": len(results)}


@app.get("/conversations/show")
async def show_conversation(conversation_id: int) -> dict:
    conversation = find_by_id(conversations, conversation_id)
    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    conversation_messages = []
    for message in messages:
        if message["conversation_id"] == conversation_id:
            conversation_messages.append(message)

    return {
        "conversation": conversation,
        "messages": conversation_messages,
        "count": len(conversation_messages),
    }


@app.post("/messages/ask")
async def ask_question(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    missing = find_missing_field(json_body, ["conversation_id", "text"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}

    conversation_id = json_body["conversation_id"]
    conversation = find_by_id(conversations, conversation_id)
    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    new_message = {
        "id": get_next_id(messages),
        "conversation_id": conversation_id,
        "sender_type": "user",
        "sender_id": conversation["user_id"],
        "text": json_body["text"],
        "reply_to": None,
    }
    messages.append(new_message)
    return {"message": "Query saved!", "chat_message": new_message}


@app.post("/messages/reply")
async def reply_to_question(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    missing = find_missing_field(json_body, ["reply_to"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}

    reply_to = json_body["reply_to"]
    query = find_by_id(messages, reply_to)
    if query is None or query["sender_type"] != "user":
        return {"error": f"User message {reply_to} not found"}

    if has_reply(messages, reply_to):
        return {"error": f"Message {reply_to} already has a reply"}

    conversation = find_by_id(conversations, query["conversation_id"])
    new_message = {
        "id": get_next_id(messages),
        "conversation_id": query["conversation_id"],
        "sender_type": "bot",
        "sender_id": conversation["bot_id"],
        "text": choice(bot_replies),
        "reply_to": reply_to,
    }
    messages.append(new_message)
    return {"message": "Reply saved!", "chat_message": new_message}


@app.get("/messages")
async def view_messages(
    conversation_id: int | None = None, sender_type: str | None = None
) -> dict:
    results = []
    for message in messages:
        if (
            conversation_id is not None
            and message["conversation_id"] != conversation_id
        ):
            continue
        if sender_type is not None and message["sender_type"] != sender_type:
            continue
        results.append(message)
    return {"messages": results, "count": len(results)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
