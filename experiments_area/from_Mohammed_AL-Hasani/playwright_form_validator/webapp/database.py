import sqlite3
from pathlib import Path

from webapp.passwords import hash_password, verify_password

DATABASE_PATH = Path(__file__).with_name("users.db")
UNKNOWN_USER_HASH = hash_password("not-a-real-password")


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_PATH)


def seed_users(users: dict[str, str]) -> None:
    """Create the users table and store each user with a salted password hash."""
    with _connect() as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)"
        )
        for username, password in users.items():
            connection.execute(
                "INSERT OR REPLACE INTO users (username, password_hash) VALUES (?, ?)",
                (username, hash_password(password)),
            )


def credentials_are_valid(username: str, password: str) -> bool:
    """Look the user up with a parameterised query and verify the password."""
    with _connect() as connection:
        row = connection.execute(
            "SELECT password_hash FROM users WHERE username = ?", (username,)
        ).fetchone()
    stored_hash = row[0] if row else UNKNOWN_USER_HASH
    password_matches = verify_password(password, stored_hash)
    return row is not None and password_matches
