import uvicorn
from random import randint
from fastapi import FastAPI, Request
from chat_data import (
    users, bots, messages, conversations, bot_replies,
    find_by_id, next_id, find_missing_field, find_reply
)

app = FastAPI()


async def read_json_body(incoming_request: Request) -> dict:
    """Return the JSON body as a dict, or an empty dict if the body is not valid JSON."""
    try:
        json_body = await incoming_request.json()
    except ValueError:
        return {}
    if not isinstance(json_body, dict):
        return {}
    return json_body


# ---------- Users ----------

@app.post("/users/add")
async def add_user(incoming_request: Request) -> dict:
    json_body = await read_json_body(incoming_request)
    missing_field = find_missing_field(json_body, ["name"])
    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    new_user = {"id": next_id(users), "name": json_body.get("name")}
    users.append(new_user)
    return {"message": "User added successfully!", "user": new_user}


@app.get("/users")
async def get_users(user_id: int | None = None) -> dict:
    if user_id is None:
        return {"users": users, "count": len(users)}

    user = find_by_id(users, user_id)
    if user is None:
        return {"error": f"User {user_id} not found"}
    return {"user": user}


# ---------- Bots ----------

@app.post("/bots/add")
async def add_bot(incoming_request: Request) -> dict:
    json_body = await read_json_body(incoming_request)
    missing_field = find_missing_field(json_body, ["name"])
    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    new_bot = {"id": next_id(bots), "name": json_body.get("name")}
    bots.append(new_bot)
    return {"message": "Bot added successfully!", "bot": new_bot}


@app.get("/bots")
async def get_bots(bot_id: int | None = None) -> dict:
    if bot_id is None:
        return {"bots": bots, "count": len(bots)}

    bot = find_by_id(bots, bot_id)
    if bot is None:
        return {"error": f"Bot {bot_id} not found"}
    return {"bot": bot}


# ---------- Conversations ----------

@app.post("/conversations/start")
async def start_conversation(incoming_request: Request) -> dict:
    json_body = await read_json_body(incoming_request)
    missing_field = find_missing_field(json_body, ["user_id", "bot_id"])
    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    user_id = json_body.get("user_id")
    bot_id = json_body.get("bot_id")
    if find_by_id(users, user_id) is None:
        return {"error": f"User {user_id} not found"}
    if find_by_id(bots, bot_id) is None:
        return {"error": f"Bot {bot_id} not found"}

    new_conversation = {"id": next_id(conversations), "user_id": user_id, "bot_id": bot_id}
    conversations.append(new_conversation)
    return {"message": "Conversation started!", "conversation": new_conversation}


@app.get("/conversations")
async def get_conversations(user_id: int | None = None) -> dict:
    result = []
    for conversation in conversations:
        if user_id is None or conversation["user_id"] == user_id:
            result.append(conversation)
    return {"conversations": result, "count": len(result)}


@app.get("/conversations/show")
async def show_conversation(conversation_id: int) -> dict:
    conversation = find_by_id(conversations, conversation_id)
    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    # Messages are appended to one list, so the list order is the conversation order
    conversation_messages = []
    for message in messages:
        if message["conversation_id"] == conversation_id:
            conversation_messages.append(message)
    return {
        "conversation": conversation,
        "messages": conversation_messages,
        "count": len(conversation_messages)
    }


# ---------- Messages ----------

@app.post("/messages/ask")
async def ask(incoming_request: Request) -> dict:
    json_body = await read_json_body(incoming_request)
    missing_field = find_missing_field(json_body, ["conversation_id", "text"])
    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    conversation_id = json_body.get("conversation_id")
    conversation = find_by_id(conversations, conversation_id)
    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    new_message = {
        "id": next_id(messages),
        "conversation_id": conversation_id,
        "sender_type": "user",
        "sender_id": conversation["user_id"],
        "text": json_body.get("text"),
        "reply_to": None
    }
    messages.append(new_message)
    return {"message": "Query saved!", "chat_message": new_message}


@app.post("/messages/reply")
async def reply(incoming_request: Request) -> dict:
    json_body = await read_json_body(incoming_request)
    missing_field = find_missing_field(json_body, ["reply_to"])
    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    reply_to = json_body.get("reply_to")
    query = find_by_id(messages, reply_to)
    if query is None or query["sender_type"] != "user":
        return {"error": f"User message {reply_to} not found"}
    if find_reply(reply_to) is not None:
        return {"error": f"Message {reply_to} already has a reply"}

    conversation = find_by_id(conversations, query["conversation_id"])
    new_message = {
        "id": next_id(messages),
        "conversation_id": query["conversation_id"],
        "sender_type": "bot",
        "sender_id": conversation["bot_id"],
        "text": bot_replies[randint(0, len(bot_replies) - 1)],
        "reply_to": reply_to
    }
    messages.append(new_message)
    return {"message": "Reply saved!", "chat_message": new_message}


@app.get("/messages")
async def get_messages(conversation_id: int | None = None, sender_type: str | None = None) -> dict:
    result = []
    for message in messages:
        if conversation_id is not None and message["conversation_id"] != conversation_id:
            continue
        if sender_type is not None and message["sender_type"] != sender_type:
            continue
        result.append(message)
    return {"messages": result, "count": len(result)}


if __name__ == "__main__":
    # Reachable from other machines on the network for pair testing: http://<your-ip>:8000/users
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
