import os
import secrets
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pwdlib import PasswordHash
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "training_users.db"
load_dotenv(BASE_DIR / ".env")
password_hash = PasswordHash.recommended()
basic_auth = HTTPBasic(auto_error=False)
sessions: dict[str, str] = {}
app = FastAPI(title="Playwright Form Validator")


class ChatMessage(BaseModel):
    message: str = ""


def database_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    demo_password = os.getenv("DEMO_USER_PASSWORD")
    nurse_password = os.getenv("NURSE_USER_PASSWORD")
    if not demo_password or not nurse_password:
        raise RuntimeError(
            "DEMO_USER_PASSWORD and NURSE_USER_PASSWORD must be set before starting"
        )

    with database_connection() as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)"
        )
        for username, password in (
            ("demo_user", demo_password),
            ("nurse_user", nurse_password),
        ):
            existing = connection.execute(
                "SELECT username FROM users WHERE username = ?", (username,)
            ).fetchone()
            if existing is None:
                connection.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash.hash(password)),
                )


@app.on_event("startup")
def startup() -> None:
    initialize_database()


def page(name: str) -> HTMLResponse:
    return HTMLResponse((BASE_DIR / "templates" / name).read_text(encoding="utf-8"))


def current_user(request: Request) -> str | None:
    return sessions.get(request.cookies.get("session"))


@app.get("/", response_class=HTMLResponse)
def login_page() -> HTMLResponse:
    return page("login.html")


@app.post("/api/login")
def login(
    credentials: HTTPBasicCredentials | None = Depends(basic_auth),  # noqa: B008
) -> JSONResponse:
    if credentials is None or not credentials.username or not credentials.password:
        return JSONResponse({"message": "Username and password are required"})

    with database_connection() as connection:
        user = connection.execute(
            "SELECT username, password_hash FROM users WHERE username = ?",
            (credentials.username,),
        ).fetchone()

    if user is None or not password_hash.verify(
        credentials.password, user["password_hash"]
    ):
        return JSONResponse({"message": "Invalid username or password"})

    session_id = secrets.token_urlsafe(32)
    sessions[session_id] = user["username"]
    response = JSONResponse({"message": f"Welcome, {user['username']}"})
    response.set_cookie("session", session_id, httponly=True, samesite="lax")
    return response


@app.get("/chat", response_class=HTMLResponse, response_model=None)
def chat_page(request: Request) -> HTMLResponse | RedirectResponse:
    if current_user(request) is None:
        return RedirectResponse("/", status_code=303)
    return page("chat.html")


@app.post("/api/chat")
def chat(request: Request, payload: ChatMessage) -> JSONResponse:
    if current_user(request) is None:
        return JSONResponse({"error": "Authentication required"}, status_code=401)
    message = payload.message
    if not message.strip():
        return JSONResponse({"error": "Message cannot be empty"})
    if len(message) > 200:
        return JSONResponse({"error": "Message too long"})
    return JSONResponse({"message": message})
