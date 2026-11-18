import base64
import binascii
import json
import secrets
import sqlite3
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from passwords import is_password_correct

DATABASE_PATH = Path(__file__).with_name("users.db")
HOST = "127.0.0.1"
PORT = 8000
MAX_MESSAGE_LENGTH = 200

sessions: dict[str, str] = {}

LOGIN_PAGE = """<!DOCTYPE html>
<html>
<head><title>Clinic Login</title></head>
<body>
  <h1>Clinic Login</h1>
  <label for="username">Username</label>
  <input id="username" type="text">
  <label for="password">Password</label>
  <input id="password" type="password">
  <button id="login-button" type="button">Log in</button>
  <p id="login-result"></p>
  <a id="chat-link" href="/chat" hidden>Go to chat</a>
  <script>
    document.getElementById("login-button").addEventListener("click", async () => {
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const response = await fetch("/login", {
        method: "POST",
        headers: { "Authorization": "Basic " + btoa(username + ":" + password) },
      });
      const data = await response.json();
      document.getElementById("login-result").textContent = data.message;
      document.getElementById("chat-link").hidden = !data.ok;
    });
  </script>
</body>
</html>"""

CHAT_PAGE = """<!DOCTYPE html>
<html>
<head><title>Clinic Chat</title></head>
<body>
  <h1>Clinic Chat</h1>
  <ul id="chat-log"></ul>
  <label for="chat-message">Message</label>
  <input id="chat-message" type="text">
  <button id="send-button" type="button">Send</button>
  <p id="chat-error"></p>
  <script>
    document.getElementById("send-button").addEventListener("click", async () => {
      const messageInput = document.getElementById("chat-message");
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: messageInput.value }),
      });
      const data = await response.json();
      const errorBox = document.getElementById("chat-error");
      if (data.ok) {
        const item = document.createElement("li");
        item.textContent = data.message;
        document.getElementById("chat-log").appendChild(item);
        errorBox.textContent = "";
        messageInput.value = "";
      } else {
        errorBox.textContent = data.message;
      }
    });
  </script>
</body>
</html>"""


def read_basic_auth(header: str) -> tuple[str, str]:
    """Turn 'Basic <base64 of username:password>' back into (username, password)."""
    if not header.startswith("Basic "):
        return "", ""
    try:
        decoded = base64.b64decode(header.removeprefix("Basic ")).decode()
    except (binascii.Error, UnicodeDecodeError):
        return "", ""
    username, _, password = decoded.partition(":")
    return username, password


def check_login(username: str, password: str) -> tuple[bool, str]:
    if not username or not password:
        return False, "Username and password are required"
    connection = sqlite3.connect(DATABASE_PATH)
    row = connection.execute(
        "SELECT salt, password_hash FROM users WHERE username = ?", (username,)
    ).fetchone()
    connection.close()
    if row is None or not is_password_correct(password, row[0], row[1]):
        return False, "Invalid username or password"
    return True, f"Welcome, {username}"


def check_chat_message(message: str) -> tuple[bool, str]:
    if not message.strip():
        return False, "Message cannot be empty"
    if len(message) > MAX_MESSAGE_LENGTH:
        return False, "Message too long"
    return True, message


class ClinicHandler(BaseHTTPRequestHandler):
    def logged_in_user(self) -> str | None:
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        if "session" not in cookie:
            return None
        return sessions.get(cookie["session"].value)

    def send_html(self, page: str) -> None:
        body = page.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status: int, ok: bool, message: str, session_token: str = "") -> None:
        body = json.dumps({"ok": ok, "message": message}).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        if session_token:
            self.send_header("Set-Cookie", f"session={session_token}; HttpOnly; Path=/")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/":
            self.send_html(LOGIN_PAGE)
        elif self.path == "/chat":
            if self.logged_in_user() is None:
                self.send_response(303)
                self.send_header("Location", "/")
                self.end_headers()
            else:
                self.send_html(CHAT_PAGE)
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        if self.path == "/login":
            username, password = read_basic_auth(self.headers.get("Authorization", ""))
            ok, message = check_login(username, password)
            if ok:
                token = secrets.token_hex(16)
                sessions[token] = username
                self.send_json(200, True, message, token)
            else:
                self.send_json(401, False, message)
        elif self.path == "/chat":
            if self.logged_in_user() is None:
                self.send_json(401, False, "Please log in first")
                return
            length = int(self.headers.get("Content-Length", "0"))
            try:
                message = json.loads(self.rfile.read(length)).get("message", "")
            except json.JSONDecodeError:
                message = ""
            ok, reply = check_chat_message(str(message))
            self.send_json(200 if ok else 400, ok, reply)
        else:
            self.send_error(404)


def main() -> None:
    if not DATABASE_PATH.exists():
        print("users.db not found. Run seed_users.py first.")
        return
    server = ThreadingHTTPServer((HOST, PORT), ClinicHandler)
    print(f"Clinic app running on http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
