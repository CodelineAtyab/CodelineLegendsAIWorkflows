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
        return