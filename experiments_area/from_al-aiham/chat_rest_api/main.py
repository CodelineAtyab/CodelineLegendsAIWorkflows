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
async def add_user(incoming_request: Request) -> dict:
    """Add a user when the required name is supplied."""
    body = await incoming_request.json()
    missing_field = get_missing_field(body, ("name",))

    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    user = {"id": get_next_id(users), "name": body["name"]}
    users.append(user)

    return {"message": "User added successfully!", "user": user}


@app.get("/users")
async def get_users(user_id: int | None = None) -> dict:
    """Return all users or the user with the requested ID."""
    if user_id is None:
        return {"users": users, "count": len(users)}

    user = find_by_id(users, user_id)

    if user is None:
        return {"error": f"User {user_id} not found"}

    return {"user": user}


@app.post("/bots/add")
async def add_bot(incoming_request: Request) -> dict:
    """Add a bot when the required name is supplied."""
    body = await incoming_request.json()
    missing_field = get_missing_field(body, ("name",))

    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    bot = {"id": get_next_id(bots), "name": body["name"]}
    bots.append(bot)

    return {"message": "Bot added successfully!", "bot": bot}


@app.get("/bots")
async def get_bots(bot_id: int | None = None) -> dict:
    """Return all bots or the bot with the requested ID."""
    if bot_id is None:
        return {"bots": bots, "count": len(bots)}

    bot = find_by_id(bots, bot_id)

    if bot is None:
        return {"error": f"Bot {bot_id} not found"}

    return {"bot": bot}


@app.post("/conversations/start")
async def start_conversation(incoming_request: Request) -> dict:
    """Start a conversation between an existing user and an existing bot."""
    body = await incoming_request.json()
    missing_field = get_missing_field(body, ("user_id", "bot_id"))

    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    user_id = body["user_id"]
    bot_id = body["bot_id"]

    if find_by_id(users, user_id) is None:
        return {"error": f"User {user_id} not found"}

    if find_by_id(bots, bot_id) is None:
        return {"error": f"Bot {bot_id} not found"}

    conversation = {
        "id": get_next_id(conversations),
        "user_id": user_id,
        "bot_id": bot_id,
    }
    conversations.append(conversation)

    return {"message": "Conversation started!", "conversation": conversation}


@app.get("/conversations")
async def get_conversations(user_id: int | None = None) -> dict:
    """Return all conversations or only those belonging to one user."""
    result = []

    for conversation in conversations:
        if user_id is not None and conversation["user_id"] != user_id:
            continue

        result.append(conversation)

    return {"conversations": result, "count": len(result)}


@app.get("/conversations/show")
async def show_conversation(conversation_id: int) -> dict:
    """Return a conversation and its messages in creation order."""
    conversation = find_by_id(conversations, conversation_id)

    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    result = filter_messages(conversation_id=conversation_id)

    return {
        "conversation": conversation,
        "messages": result,
        "count": len(result),
    }


@app.post("/messages/ask")
async def ask_message(incoming_request: Request) -> dict:
    """Save a query from the conversation's user without generating a reply."""
    body = await incoming_request.json()
    missing_field = get_missing_field(body, ("conversation_id", "text"))

    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    conversation_id = body["conversation_id"]
    conversation = find_by_id(conversations, conversation_id)

    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    message = {
        "id": get_next_id(messages),
        "conversation_id": conversation_id,
        "sender_type": "user",
        "sender_id": conversation["user_id"],
        "text": body["text"],
        "reply_to": None,
    }
    messages.append(message)

    return {"message": "Query saved!", "chat_message": message}


@app.post("/messages/reply")
async def reply_message(incoming_request: Request) -> dict:
    """Save one random canned reply to an unanswered user query."""
    body = await incoming_request.json()
    missing_field = get_missing_field(body, ("reply_to",))

    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    reply_to = body["reply_to"]
    query = find_by_id(messages, reply_to)

    if query is None or query["sender_type"] != "user":
        return {"error": f"User message {reply_to} not found"}

    if has_reply(reply_to):
        return {"error": f"Message {reply_to} already has a reply"}

    conversation = find_by_id(conversations, query["conversation_id"])

    if conversation is None:
        return {"error": f"Conversation {query['conversation_id']} not found"}

    message = {
        "id": get_next_id(messages),
        "conversation_id": conversation["id"],
        "sender_type": "bot",
        "sender_id": conversation["bot_id"],
        "text": choice(bot_replies),
        "reply_to": reply_to,
    }
    messages.append(message)

    return {"message": "Reply saved!", "chat_message": message}


@app.get("/messages")
async def get_messages(
    conversation_id: int | None = None,
    sender_type: str | None = None,
) -> dict:
    """Return messages matching the optional conversation and sender filters."""
    result = filter_messages(conversation_id, sender_type)
    return {"messages": result, "count": len(result)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)