import uvicorn
from fastapi import FastAPI, Request
from chat_data import users, bots, find_by_id, next_id, find_missing_field

app = FastAPI()


@app.post("/users/add")
async def add_user(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()
    missing_field = find_missing_field(json_body, ["name"])
    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    new_user = {"id": next_id(users), "name": json_body.get("name")}
    users.append(new_user)
    return {"message": "User added successfully!", "user": new_user}


@app.get("/users")
async def get_users(user_id: int | None = None) -> dict:
    if user_id is not None:
        user = find_by_id(users, user_id)
        if user is None:
            return {"error": f"User {user_id} not found"}
        return {"user": user}

    return {"users": users, "count": len(users)}


@app.post("/bots/add")
async def add_bot(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()
    missing_field = find_missing_field(json_body, ["name"])
    if missing_field is not None:
        return {"error": f"Missing field: {missing_field}"}

    new_bot = {"id": next_id(bots), "name": json_body.get("name")}
    bots.append(new_bot)
    return {"message": "Bot added successfully!", "bot": new_bot}


@app.get("/bots")
async def get_bots(bot_id: int | None = None) -> dict:
    if bot_id is not None:
        bot = find_by_id(bots, bot_id)
        if bot is None:
            return {"error": f"Bot {bot_id} not found"}
        return {"bot": bot}

    return {"bots": bots, "count": len(bots)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
