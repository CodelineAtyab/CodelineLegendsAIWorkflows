import uvicorn
from fastapi import FastAPI
from models.users_model import User

app = FastAPI()

@app.post("/users")
def register_user(currUser: User) -> User:
    return currUser


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
