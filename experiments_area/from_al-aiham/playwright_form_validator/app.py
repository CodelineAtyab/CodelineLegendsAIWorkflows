import base64
import binascii
from contextlib import closing
import hashlib
import hmac
from http import HTTPStatus
from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import sqlite3


PROJECT_DIR = Path(__file__).resolve().parent
DATABASE = PROJECT_DIR / "users.db"
SESSIONS: dict[str, str] = {}


def password_hash(password: str, salt: bytes) -> str:
    return hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1
    ).hex()


def seed_users() -> None:
    with closing(sqlite3.connect(DATABASE)) as connection, connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(username TEXT PRIMARY KEY, salt TEXT NOT NULL, password_hash TEXT NOT NULL)"
        )
        for username, variable in (
            ("demo_user", "DEMO_PASSWORD"),
            ("nurse_user", "NURSE_PASSWORD"),
        ):
            if connection.execute(
                "SELECT username FROM users WHERE username = ?", (username,)
            ).fetchone():
                continue
            password = os.environ.get(variable)
            if not password:
                raise ValueError(f"Set {variable} to a made-up training password before starting the app.")
            salt = os.urandom(16)
            connection.execute(
                "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
                (username, salt.hex(), password_hash(password, salt)),
            )


class FormHandler(BaseHTTPRequestHandler):
    def respond(self, status: HTTPStatus, body: str, content_type: str, cookie: str = "") -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(encoded)

    def json_response(self, status: HTTPStatus, message: str, cookie: str = "") -> None:
        self.respond(status, json.dumps({"message": message}), "application/json", cookie)

    def session_token(self) -> str:
        cookies = SimpleCookie()
        try:
            cookies.load(self.headers.get("Cookie", ""))
        except CookieError:
            return ""
        session = cookies.get("session")
        return session.value if session else ""

    def do_GET(self) -> None:
        if self.path == "/chat" and self.session_token() not in SESSIONS:
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", "/")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        pages = {"/": "login.html", "/chat": "chat.html"}
        if self.path not in pages:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self.respond(
            HTTPStatus.OK,
            (PROJECT_DIR / pages[self.path]).read_text(encoding="utf-8"),
            "text/html",
        )

    def do_POST(self) -> None:
        if self.path == "/api/login":
            self.login()
        elif self.path == "/api/chat":
            self.chat()
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def login(self) -> None:
        SESSIONS.pop(self.session_token(), None)
        clear_cookie = "session=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0"
        authorization = self.headers.get("Authorization", "")
        scheme, _, value = authorization.partition(" ")
        try:
            if scheme.lower() != "basic":
                raise ValueError("Basic authentication is required")
            decoded = base64.b64decode(value, validate=True).decode("utf-8")
            username, password = decoded.split(":", 1)
        except (ValueError, UnicodeDecodeError, binascii.Error):
            self.json_response(HTTPStatus.UNAUTHORIZED, "Invalid username or password", clear_cookie)
            return
        username = username.strip()
        if not username or not password:
            self.json_response(HTTPStatus.BAD_REQUEST, "Username and password are required", clear_cookie)
            return
        with closing(sqlite3.connect(DATABASE)) as connection:
            user = connection.execute(
                "SELECT salt, password_hash FROM users WHERE username = ?", (username,)
            ).fetchone()
        if not user or not hmac.compare_digest(
            password_hash(password, bytes.fromhex(user[0])), user[1]
        ):
            self.json_response(HTTPStatus.UNAUTHORIZED, "Invalid username or password", clear_cookie)
            return
        token = secrets.token_urlsafe(32)
        SESSIONS[token] = username
        self.json_response(
            HTTPStatus.OK,
            f"Welcome, {username}",
            f"session={token}; Path=/; HttpOnly; SameSite=Strict",
        )

    def chat(self) -> None:
        if self.session_token() not in SESSIONS:
            self.json_response(HTTPStatus.UNAUTHORIZED, "Please log in first")
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(size))
        except (ValueError, UnicodeDecodeError):
            self.json_response(HTTPStatus.BAD_REQUEST, "Invalid message")
            return
        message = payload.get("message") if isinstance(payload, dict) else None
        if not isinstance(message, str) or not message.strip():
            self.json_response(HTTPStatus.BAD_REQUEST, "Message cannot be empty")
        elif len(message) > 200:
            self.json_response(HTTPStatus.BAD_REQUEST, "Message too long")
        else:
            self.json_response(HTTPStatus.OK, message)


def main() -> None:
    try:
        seed_users()
    except ValueError as error:
        print(error)
        return
    with ThreadingHTTPServer(("localhost", 8000), FormHandler) as server:
        print("Training forms running at http://localhost:8000")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
