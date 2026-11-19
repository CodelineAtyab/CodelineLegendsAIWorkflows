import base64
import binascii
import os
import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Header
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from webapp.database import credentials_are_valid, seed_users

STATIC_DIR = Path(__file__).with_name("static")
MAX_MESSAGE_LENGTH = 200

REQUIRED_MESSAGE = "Username and password are required"
INVALID_MESSAGE = "Invalid username or password"
EMPTY_CHAT_MESSAGE = "Message cannot be empty"
LONG_CHAT_MESSAGE = "Message too long"

SEED_PASSWORD_VARIABLES = {
    "demo_user": "DEMO_USER_PASSWORD",
    "nurse_user": "NURSE_USER_PASSWORD",
}

app = FastAPI(title="Login and Chat Demo")


class ChatRequest(BaseModel):
    message: str


def parse_basic_auth(authorization: str | None) -> tuple[str, str]:
    """Split an "Authorization: Basic ..." header into (username, password)."""
    if not authorization or not authorization.startswith("Basic "):
        return "", ""
    try:
        decoded = base64.b64decode(authorization[len("Basic "):]).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        return "", ""
    username, _, password = decoded.partition(":")
    return username, password


def reject(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"message": message})


def check_login(authorization: str | None) -> tuple[str, JSONResponse | None]:
    """Return (username, None) on success, or ("", error response) on failure."""
    username, password = parse_basic_auth(authorization)
    if not username or not password:
        return "", reject(400, REQUIRED_MESSAGE)
    if not credentials_are_valid(username, password):
        return "", reject(401, INVALID_MESSAGE)
    return username, None


@app.get("/")
def login_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "login.html")


@app.get("/favicon.ico")
def favicon() -> Response:
    return Response(status_code=204)


@app.get("/chat")
def chat_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "chat.html")


@app.post("/api/login")
def login(authorization: str | None = Header(default=None)) -> JSONResponse:
    username, error = check_login(authorization)
    if error:
        return error
    return JSONResponse(content={"message": f"Welcome, {username}"})


@app.post("/api/chat")
def chat(
    request: ChatRequest, authorization: str | None = Header(default=None)
) -> JSONResponse:
    _, error = check_login(authorization)
    if error:
        return error
    if not request.message.strip():
        return reject(400, EMPTY_CHAT_MESSAGE)
    if len(request.message) > MAX_MESSAGE_LENGTH:
        return reject(400, LONG_CHAT_MESSAGE)
    return JSONResponse(content={"message": request.message})


def load_seed_users() -> dict[str, str]:
    """Read the fake training passwords from the environment, never from code."""
    load_dotenv()
    missing = [name for name in SEED_PASSWORD_VARIABLES.values() if not os.getenv(name)]
    if missing:
        sys.exit(f"Set these environment variables first: {', '.join(missing)}")
    return {
        username: os.environ[variable]
        for username, variable in SEED_PASSWORD_VARIABLES.items()
    }


if __name__ == "__main__":
    seed_users(load_seed_users())
    uvicorn.run(app, host="127.0.0.1", port=8000)
