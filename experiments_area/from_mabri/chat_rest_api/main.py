from random import choice

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


async def read_body(incoming_request: Request) -> dict:
    # An empty or non-JSON body becomes {}, so the route answers
    # "Missing field: ..." instead of crashing with a 500.
    try:
        body = await incoming_request.json()
    except ValueError:
        return {}
    if not isinstance(body, dict):
        return {}
    return body


@app.get("/users")
async def get_users(user_id: int | None = None) -> dict:
    if user_id is not None:
        user = find_by_id(users, user_id)
        if user is None:
            return {"error": f"User {user_id} not found"}
        return {"user": user}
    return {"users": users}


@app.post("/users/add")
async def add_user(incoming_request: Request) -> dict:
    body = await read_body(incoming_request)
    missing = missing_field(body, ["name"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}
    new_user = {"id": next_id(users), "name": body["name"]}
    users.append(new_user)
    return {"message": "User added successfully!", "user": new_user}


@app.post("/bots/add")
async def add_bot(incoming_request: Request) -> dict:
    body = await read_body(incoming_request)
    missing = missing_field(body, ["name"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}
    new_bot = {"id": next_id(bots), "name": body["name"]}
    bots.append(new_bot)
    return {"message": "Bot added successfully!", "bot": new_bot}


@app.get("/bots")
async def get_bots(bot_id: int | None = None) -> dict:
    if bot_id is not None:
        bot = find_by_id(bots, bot_id)
        if bot is None:
            return {"error": f"Bot {bot_id} not found"}
        return {"bot": bot}
    return {"bots": bots}


@app.post("/conversations/start")
async def start_conversation(incoming_request: Request) -> dict:
    body = await read_body(incoming_request)
    missing = missing_field(body, ["user_id", "bot_id"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}
    user_id = body["user_id"]
    bot_id = body["bot_id"]
    if find_by_id(users, user_id) is None:
        return {"error": f"User {user_id} not found"}
    if find_by_id(bots, bot_id) is None:
        return {"error": f"Bot {bot_id} not found"}
    new_conversation = {
        "id": next_id(conversations),
        "user_id": user_id,
        "bot_id": bot_id,
    }
    conversations.append(new_conversation)
    return {"message": "Conversation started!", "conversation": new_conversation}


@app.get("/conversations")
async def get_conversations(user_id: int | None = None) -> dict:
    if user_id is None:
        return {"conversations": conversations}
    result = []
    for conversation in conversations:
        if conversation["user_id"] == user_id:
            result.append(conversation)
    return {"conversations": result}


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
async def ask(incoming_request: Request) -> dict:
    body = await read_body(incoming_request)
    missing = missing_field(body, ["conversation_id", "text"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}
    conversation_id = body["conversation_id"]
    conversation = find_by_id(conversations, conversation_id)
    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}
    new_message = {
        "id": next_id(messages),
        "conversation_id": conversation_id,
        "sender_type": "user",
        "sender_id": conversation["user_id"],
        "text": body["text"],
        "reply_to": None,
    }
    messages.append(new_message)
    return {"message": "Query saved!", "chat_message": new_message}


@app.post("/messages/reply")
async def reply(incoming_request: Request) -> dict:
    body = await read_body(incoming_request)
    missing = missing_field(body, ["reply_to"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}
    reply_to = body["reply_to"]
    query = find_by_id(messages, reply_to)
    if query is None or query["sender_type"] != "user":
        return {"error": f"User message {reply_to} not found"}
    for message in messages:
        if message["reply_to"] == reply_to:
            return {"error": f"Message {reply_to} already has a reply"}
    conversation = find_by_id(conversations, query["conversation_id"])
    if conversation is None:
        return {"error": f"Conversation {query['conversation_id']} not found"}
    new_message = {
        "id": next_id(messages),
        "conversation_id": query["conversation_id"],
        "sender_type": "bot",
        "sender_id": conversation["bot_id"],
        "text": choice(bot_replies),
        "reply_to": reply_to,
    }
    messages.append(new_message)
    return {"message": "Reply saved!", "chat_message": new_message}


@app.get("/messages")
async def get_messages(
    conversation_id: int | None = None, sender_type: str | None = None
) -> dict:
    result = []
    for message in messages:
        if conversation_id is not None and message["conversation_id"] != conversation_id:
            continue
        if sender_type is not None and message["sender_type"] != sender_type:
            continue
        result.append(message)
    return {"messages": result, "count": len(result)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
