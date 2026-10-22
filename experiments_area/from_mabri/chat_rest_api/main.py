from fastapi import FastAPI, Request
from chat_data import users, bots, find_by_id, missing_field, next_id

import uvicorn

app = FastAPI()


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
    body = await incoming_request.json()
    missing = missing_field(body, ["name"])
    if missing is not None:
        return {"error": f"Missing field: {missing}"}
    new_user = {"id": next_id(users), "name": body["name"]}
    users.append(new_user)
    return {"message": "User added successfully!", "user": new_user}


@app.post("/bots/add")
async def add_bot(incoming_request: Request) -> dict:
    body = await incoming_request.json()
    missing = missing_field(body, ["name"])
    if missing is None:
        return {"error": f"Missing field: {missing}"}
    new_bot = {"id": next_id(bots), "name": body["name"]}
    users.append(new_bot)
    return {"message": "Bot added successfully!", "bot": new_bot}


@app.get("/bots")
async def get_bots(bot_id: int | None = None) -> dict:
    if bot_id is not None:
        bot = find_by_id(bots, bot_id)
        if bot is None:
            return {"error": f"Bot {bot_id} not found"}
        return {"bot": bot}
    return {"bots": bots}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
