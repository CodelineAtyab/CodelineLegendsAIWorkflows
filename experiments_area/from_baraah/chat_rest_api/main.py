import uvicorn
from fastapi import FastAPI, Request

from chat_data import (
    bots,
    conversations,
    find_by_id,
    get_bot_reply,
    messages,
    missing_field,
    next_id,
    users,
)

app = FastAPI()


# 1. Add User
@app.post("/users/add")
async def add_user(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    missing = missing_field(json_body, ["name"])

    if missing:
        return {"error": f"Missing field: {missing}"}

    new_user = {
        "id": next_id(users),
        "name": json_body.get("name"),
    }

    users.append(new_user)

    return {
        "message": "User added successfully!",
        "user": new_user,
    }


# 2. Get Users
@app.get("/users")
async def get_users(user_id: int | None = None) -> dict:
    if user_id is not None:
        user = find_by_id(users, user_id)

        if user is None:
            return {"error": f"User {user_id} not found"}

        return {
            "users": [user],
            "count": 1,
        }

    return {
        "users": users,
        "count": len(users),
    }


# 3. Add Bot
@app.post("/bots/add")
async def add_bot(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    missing = missing_field(json_body, ["name"])

    if missing:
        return {"error": f"Missing field: {missing}"}

    new_bot = {
        "id": next_id(bots),
        "name": json_body.get("name"),
    }

    bots.append(new_bot)

    return {
        "message": "Bot added successfully!",
        "bot": new_bot,
    }


# 4. Get Bots
@app.get("/bots")
async def get_bots(bot_id: int | None = None) -> dict:
    if bot_id is not None:
        bot = find_by_id(bots, bot_id)

        if bot is None:
            return {"error": f"Bot {bot_id} not found"}

        return {
            "bots": [bot],
            "count": 1,
        }

    return {
        "bots": bots,
        "count": len(bots),
    }


# 5. Start Conversation
@app.post("/conversations/start")
async def start_conversation(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    missing = missing_field(json_body, ["user_id", "bot_id"])

    if missing:
        return {"error": f"Missing field: {missing}"}

    user_id = json_body.get("user_id")
    bot_id = json_body.get("bot_id")

    user = find_by_id(users, user_id)

    if user is None:
        return {"error": f"User {user_id} not found"}

    bot = find_by_id(bots, bot_id)

    if bot is None:
        return {"error": f"Bot {bot_id} not found"}

    new_conversation = {
        "id": next_id(conversations),
        "user_id": user_id,
        "bot_id": bot_id,
    }

    conversations.append(new_conversation)

    return {
        "message": "Conversation started!",
        "conversation": new_conversation,
    }


# 6. Get Conversations
@app.get("/conversations")
async def get_conversations(user_id: int | None = None) -> dict:
    results = []

    for conversation in conversations:
        if user_id is not None and conversation["user_id"] != user_id:
            continue

        results.append(conversation)

    return {
        "conversations": results,
        "count": len(results),
    }


# 7. Show Conversation
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


# 8. Ask Question
@app.post("/messages/ask")
async def ask_question(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    missing = missing_field(json_body, ["conversation_id", "text"])

    if missing:
        return {"error": f"Missing field: {missing}"}

    conversation_id = json_body.get("conversation_id")
    question_text = json_body.get("text")

    conversation = find_by_id(conversations, conversation_id)

    if conversation is None:
        return {"error": f"Conversation {conversation_id} not found"}

    new_message = {
        "id": next_id(messages),
        "conversation_id": conversation_id,
        "sender_type": "user",
        "sender_id": conversation["user_id"],
        "text": question_text,
        "reply_to": None,
    }

    messages.append(new_message)

    return {
        "message": "Query saved!",
        "chat_message": new_message,
    }


# 9. Bot Reply
@app.post("/messages/reply")
async def reply_message(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    missing = missing_field(json_body, ["reply_to"])

    if missing:
        return {"error": f"Missing field: {missing}"}

    reply_to = json_body.get("reply_to")

    user_message = find_by_id(messages, reply_to)

    if user_message is None:
        return {"error": f"User message {reply_to} not found"}

    if user_message["sender_type"] != "user":
        return {"error": f"User message {reply_to} not found"}

    # A question can have only one bot reply
    for message in messages:
        if message["reply_to"] == reply_to:
            return {"error": f"Message {reply_to} already has a reply"}

    conversation = find_by_id(
        conversations,
        user_message["conversation_id"],
    )

    # Check if the conversation exists
    if conversation is None:
        return {"error": f"Conversation {user_message['conversation_id']} not found"}

    new_message = {
        "id": next_id(messages),
        "conversation_id": conversation["id"],
        "sender_type": "bot",
        "sender_id": conversation["bot_id"],
        "text": get_bot_reply(),
        "reply_to": reply_to,
    }

    messages.append(new_message)

    return {
        "message": "Reply saved!",
        "chat_message": new_message,
    }


# 10. Get Messages
@app.get("/messages")
async def get_messages(
    conversation_id: int | None = None,
    sender_type: str | None = None,
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

    return {
        "messages": results,
        "count": len(results),
    }


# Run
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
