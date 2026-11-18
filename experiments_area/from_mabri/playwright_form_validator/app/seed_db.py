"""Create users.db and seed the two fake training users.

Passwords are read from .env (DEMO_USER_PASSWORD, NURSE_USER_PASSWORD) so no
password ever appears in the code. Only a salted bcrypt hash is stored.

Run from the project folder:  uv run python app/seed_db.py
"""

import os
import sqlite3
import sys
from pathlib import Path

import bcrypt
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "users.db"

SEED_USERS = {
    "demo_user": "DEMO_USER_PASSWORD",
    "nurse_user": "NURSE_USER_PASSWORD",
}


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed() -> None:
    load_dotenv(PROJECT_DIR / ".env")
    missing = [env_name for env_name in SEED_USERS.values() if not os.getenv(env_name)]
    if missing:
        sys.exit(f"Set {', '.join(missing)} in .env first (see .env.example).")

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            " username TEXT PRIMARY KEY,"
            " password_hash TEXT NOT NULL)"
        )
        for username, env_name in SEED_USERS.items():
            connection.execute(
                "INSERT OR REPLACE INTO users (username, password_hash) VALUES (?, ?)",
                (username, hash_password(os.environ[env_name])),
            )
    print(f"Seeded {len(SEED_USERS)} users into {DB_PATH.name}")


if __name__ == "__main__":
    seed()
