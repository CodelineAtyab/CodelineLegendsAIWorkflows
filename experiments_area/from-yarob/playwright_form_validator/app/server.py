import base64
import binascii
import json
import secrets
import sqlite3
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from password_hashing import verify_password

HOST = "localhost"
PORT = 8000
APP_DIR = Path(__file__).parent
DATABASE_PATH = APP_DIR / "users.db"
PAGES_DIR = APP_DIR / "pages"
SESSION_COOKIE = "session_id"
MAX_MESSAGE_LENGTH = 200

MISSING_CREDENTIALS = "Username and password are required"
INVALID_CREDENTIALS = "Invalid username or password"
EMPTY_MESSAGE = "Message cannot be empty"
MESSAGE_TOO_LONG = "Message too long"

active_sessions: dict[str, str] = {}


def read_basic_auth(header_value: str | None) -> tuple[str, str] | None:
    if not header_value or not header_value.startswith("Basic "):
        return None
    try:
        decoded = base64.b64decode(header_value.removeprefix("Basic "), validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        return None
    username, separator, password = decoded.partition(":")
    if not separator:
        return None
    return username, password


def credentials_are_valid(username: str, password: str) -> bool:
    with sqlite3.connect(DATABASE_PATH) as connection:
        row = connection.execute(
            "SELECT password_salt, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if row is None:
        return False
    salt, password_hash = row
    return verify_password(password, salt, password_hash)


class FormAppHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/":
            self.send_page("login.html")
        elif self.path == "/chat":
            if self.logged_in_user() is None:
                self.send_response(HTTPStatus.SEE_OTHER)
                self.send_header("Location", "/")
                self.end_headers()
            else:
                self.send_page("chat.html")
        else:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self) -> None:
        if self.path == "/api/login":
            self.handle_login()
        elif self.path == "/api/chat":
            self.handle_chat()
        else:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def handle_login(self) -> None:
        credentials = read_basic_auth(self.headers.get("Authorization"))
        if credentials is None:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"error": INVALID_CREDENTIALS})
            return
        username, password = credentials
        if not username or not password:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": MISSING_CREDENTIALS})
            return
        if not credentials_are_valid(username, password):
            self.send_json(HTTPStatus.UNAUTHORIZED, {"error": INVALID_CREDENTIALS})
            return
        session_id = secrets.token_urlsafe(32)
        active_sessions[session_id] = username
        cookie = f"{SESSION_COOKIE}={session_id}; HttpOnly; SameSite=Strict; Path=/"
        self.send_json(HTTPStatus.OK, {"message": f"Welcome, {username}"}, cookie)

    def handle_chat(self) -> None:
        if self.logged_in_user() is None:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "Please log in first"})
            return
        body_length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(body_length) or b"{}")
        except json.JSONDecodeError:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": EMPTY_MESSAGE})
            return
        message = str(payload.get("message", ""))
        if not message.strip():
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": EMPTY_MESSAGE})
        elif len(message) > MAX_MESSAGE_LENGTH:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": MESSAGE_TOO_LONG})
        else:
            self.send_json(HTTPStatus.OK, {"message": message})

    def logged_in_user(self) -> str | None:
        cookies = SimpleCookie(self.headers.get("Cookie", ""))
        session = cookies.get(SESSION_COOKIE)
        return active_sessions.get(session.value) if session else None

    def send_page(self, file_name: str) -> None:
        content = (PAGES_DIR / file_name).read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, status: HTTPStatus, body: dict, cookie: str | None = None) -> None:
        content = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    if not DATABASE_PATH.exists():
        raise SystemExit("users.db not found. Run: uv run app/seed_users.py")
    print(f"Form app running on http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), FormAppHandler).serve_forever()
