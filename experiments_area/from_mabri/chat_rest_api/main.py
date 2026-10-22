from fastapi import FastAPI
from chat_data import users, find_by_id

import uvicorn

app = FastAPI()


@app.get("/users")
async def get_users(user_id: int | None = None) -> dict:
    if user_id is not None:
        user = find_by_id(users, user_id)
        if user is None:
            return {"error": f"User {user_id} not found"}
        return {"users": user}
    return {"users": users}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
