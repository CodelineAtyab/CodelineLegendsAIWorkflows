import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

from password_hashing import hash_password

DATABASE_PATH = Path(__file__).parent / "users.db"
TRAINING_USERS = {
    "demo_user": "DEMO_USER_PASSWORD",
    "nurse_user": "NURSE_USER_PASSWORD",
}


def seed_users() -> None:
    load_dotenv(Path(__file__).parent.parent / ".env")
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "username TEXT PRIMARY KEY, "
            "password_salt BLOB NOT NULL, "
            "password_hash BLOB NOT NULL)"
        )
        for username, password_env_name in TRAINING_USERS.items():
            password = os.environ[password_env_name]
            salt, password_hash = hash_password(password)
            connection.execute(
                "INSERT OR REPLACE INTO users (username, password_salt, password_hash) VALUES (?, ?, ?)",
                (username, salt, password_hash),
            )
    print(f"Seeded {len(TRAINING_USERS)} users into {DATABASE_PATH.name}")


if __name__ == "__main__":
    seed_users()
