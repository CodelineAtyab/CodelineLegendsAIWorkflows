"""Tiny login + chat app used as the system under test for issue #291.

Login sends credentials as an HTTP basic authentication header; the server
checks them against salted bcrypt hashes in users.db.

Run from the project folder:  uv run uvicorn app.server:app --port 8000
"""

import base64
import binascii
import sqlite3
from pathlib import Path

import bcrypt
from fastapi import FastAPI, Header
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR.parent / "users.db"
STATIC_DIR = APP_DIR / "static"
MAX_MESSAGE_LENGTH = 200

MSG_REQUIRED = "Username and password are required"
MSG_INVALID = "Invalid username or password"
MSG_EMPTY = "Message cannot be empty"
MSG_TOO_LONG = "Message too long"

# Compared against when the username does not exist, so a wrong username takes
# as long as a wrong password and response timing does not reveal valid users.
DUMMY_HASH = bcrypt.hashpw(b"not-a-real-password", bcrypt.gensalt())

app = FastAPI(title="Clinic login and chat (training app)")
chat_log: list[dict[str, str]] = []


class ChatMessage(BaseModel):
    message: str = ""


def parse_basic_auth(authorization: str | None) -> tuple[str, str] | None:
    """Split 'Basic base64(username:password)' into its two parts."""
    if not authorization or not authorization.startswith("Basic "):
        return None
    try:
        decoded = base64.b64decode(authorization[len("Basic "):], validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        return None
    username, separator, password = decoded.partition(":")
    if not separator:
        return None
    return username, password


def find_password_hash(username: str) -> bytes | None:
    with sqlite3.connect(DB_PATH) as connection:
        row = connection.execute(
            "SELECT password_hash FROM users WHERE username = ?", (username,)
        ).fetchone()
    return row[0].encode("utf-8") if row else None


def credentials_are_valid(username: str, password: str) -> bool:
    stored_hash = find_password_hash(username)
    try:
        matches = bcrypt.checkpw(password.encode("utf-8"), stored_hash or DUMMY_HASH)
    except ValueError:  # bcrypt rejects passwords longer than 72 bytes
        return False
    return matches and stored_hash is not None


def error(status_code: int, message: str) -> JSONResponse:
    # No WWW-Authenticate header on 401: it would make the browser pop up its
    # own login dialog instead of letting our page show the message.
    return JSONResponse(status_code=status_code, content={"error": message})


def authenticate(authorization: str | None) -> str | JSONResponse:
    """Return the logged-in username, or the error response to send back."""
    credentials = parse_basic_auth(authorization)
    if credentials is None:
        return error(401, MSG_INVALID)
    username, password = credentials
    if not username or not password:
        return error(400, MSG_REQUIRED)
    if not credentials_are_valid(username, password):
        return error(401, MSG_INVALID)
    return username


@app.get("/")
def login_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "login.html")


@app.get("/chat")
def chat_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "chat.html")


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    # Empty answer so the browser console stays free of 404 noise.
    return Response(status_code=204)


@app.post("/api/login")
def login(authorization: str | None = Header(default=None)) -> JSONResponse:
    username = authenticate(authorization)
    if isinstance(username, JSONResponse):
        return username
    return JSONResponse({"message": f"Welcome, {username}"})


@app.get("/api/chat")
def read_chat(authorization: str | None = Header(default=None)) -> JSONResponse:
    username = authenticate(authorization)
    if isinstance(username, JSONResponse):
        return username
    return JSONResponse({"messages": chat_log})


@app.post("/api/chat")
def send_chat(chat: ChatMessage, authorization: str | None = Header(default=None)) -> JSONResponse:
    username = authenticate(authorization)
    if isinstance(username, JSONResponse):
        return username
    text = chat.message.strip()
    if not text:
        return error(400, MSG_EMPTY)
    if len(text) > MAX_MESSAGE_LENGTH:
        return error(400, MSG_TOO_LONG)
    chat_log.append({"username": username, "message": text})
    return JSONResponse({"messages": chat_log})
