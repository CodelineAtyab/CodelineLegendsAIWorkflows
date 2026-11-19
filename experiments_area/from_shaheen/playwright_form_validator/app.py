"""A tiny login and chat app on http://localhost:8000 to practise testing.

Run it with `uv run app.py`. Users live in users.db as a username, a random
salt and a scrypt hash. The two fake training passwords come from the
DEMO_PASSWORD and NURSE_PASSWORD environment variables.
"""

import base64
import binascii
import hashlib
import hmac
import os
import secrets
import sqlite3
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DATABASE_FILE = "users.db"
MAX_MESSAGE_LENGTH = 200
SESSIONS: dict[str, str] = {}

LOGIN_PAGE = """<!DOCTYPE html>
<html>
<head><title>Login</title><link rel="icon" href="data:,"></head>
<body>
<h1>Login</h1>
<label>Username <input id="username"></label><br>
<label>Password <input id="password" type="password"></label><br>
<button id="login-button">Log in</button>
<p id="login-result"></p>
<a id="chat-link" href="/chat" hidden>Go to chat</a>
<script>
document.getElementById("login-button").onclick = async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const response = await fetch("/login", {
        method: "POST",
        headers: {"Authorization": "Basic " + btoa(username + ":" + password)},
    });
    document.getElementById("login-result").textContent = await response.text();
    document.getElementById("chat-link").hidden = !response.ok;
};
</script>
</body>
</html>
"""

CHAT_PAGE = """<!DOCTYPE html>
<html>
<head><title>Chat</title><link rel="icon" href="data:,"></head>
<body>
<h1>Chat</h1>
<ul id="chat-log"></ul>
<input id="chat-message">
<button id="send-button">Send</button>
<p id="chat-error"></p>
<script>
document.getElementById("send-button").onclick = async () => {
    const message = document.getElementById("chat-message").value;
    const response = await fetch("/send", {method: "POST", body: message});
    const text = await response.text();
    document.getElementById("chat-error").textContent = response.ok ? "" : text;
    if (response.ok) {
        const item = document.createElement("li");
        item.textContent = text;
        document.getElementById("chat-log").appendChild(item);
        document.getElementById("chat-message").value = "";
    }
};
</script>
</body>
</html>
"""


def hash_password(password: str, salt: bytes) -> bytes:
    """Return the scrypt hash of the password with the given salt."""
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)


def seed_users() -> None:
    """Create the users table and store the two fake users with fresh salts."""
    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, salt BLOB, password_hash BLOB)"
        )
        for username, variable in [
            ("demo_user", "DEMO_PASSWORD"),
            ("nurse_user", "NURSE_PASSWORD"),
        ]:
            salt = os.urandom(16)
            connection.execute(
                "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
                (username, salt, hash_password(os.environ[variable], salt)),
            )


def check_login(username: str, password: str) -> bool:
    """Return True when the username exists and the password matches its hash."""
    with sqlite3.connect(DATABASE_FILE) as connection:
        row = connection.execute(
            "SELECT salt, password_hash FROM users WHERE username = ?", (username,)
        ).fetchone()
    if row is None:
        return False
    salt, stored_hash = row
    return hmac.compare_digest(hash_password(password, salt), stored_hash)


def read_basic_auth(header: str) -> tuple[str, str]:
    """Split an `Authorization: Basic ...` header into username and password."""
    try:
        decoded = base64.b64decode(
            header.removeprefix("Basic "), validate=True
        ).decode()
    except binascii.Error, UnicodeDecodeError:
        return "", ""
    username, _, password = decoded.partition(":")
    return username, password


class Handler(BaseHTTPRequestHandler):
    """Serve the login page, the chat page and their two form endpoints."""

    def send_text(
        self, status: int, text: str, content_type: str = "text/plain", cookie: str = ""
    ) -> None:
        """Send a response with the given status, body text and optional cookie."""
        body = text.encode()
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def logged_in(self) -> bool:
        """Return True when the request carries a session cookie from a login."""
        cookies = SimpleCookie(self.headers.get("Cookie", ""))
        return "session" in cookies and cookies["session"].value in SESSIONS

    def do_GET(self) -> None:
        """Show the login page, or the chat page after a login."""
        if self.path == "/":
            self.send_text(200, LOGIN_PAGE, "text/html")
        elif self.path == "/chat" and self.logged_in():
            self.send_text(200, CHAT_PAGE, "text/html")
        elif self.path == "/chat":
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            self.send_text(404, "Not found")

    def do_POST(self) -> None:
        """Check a login from the basic auth header, or accept a chat message."""
        if self.path == "/login":
            username, password = read_basic_auth(self.headers.get("Authorization", ""))
            if not username or not password:
                self.send_text(400, "Username and password are required")
            elif check_login(username, password):
                token = secrets.token_hex(16)
                SESSIONS[token] = username
                self.send_text(
                    200, f"Welcome, {username}", cookie=f"session={token}; HttpOnly"
                )
            else:
                self.send_text(401, "Invalid username or password")
        elif self.path == "/send" and self.logged_in():
            length = int(self.headers.get("Content-Length", 0))
            message = self.rfile.read(length).decode()
            if not message.strip():
                self.send_text(400, "Message cannot be empty")
            elif len(message) > MAX_MESSAGE_LENGTH:
                self.send_text(400, "Message too long")
            else:
                self.send_text(200, message)
        else:
            self.send_text(401, "Please log in first")


if __name__ == "__main__":
    if "DEMO_PASSWORD" not in os.environ or "NURSE_PASSWORD" not in os.environ:
        raise SystemExit(
            "Set the DEMO_PASSWORD and NURSE_PASSWORD environment variables first."
        )
    seed_users()
    print("App running on http://localhost:8000 (Ctrl+C to stop)")
    ThreadingHTTPServer(("localhost", 8000), Handler).serve_forever()
