import os
import sqlite3
from pathlib import Path

from passwords import make_password_record

DATABASE_PATH = Path(__file__).with_name("users.db")
TRAINING_USERS = {
    "demo_user": "DEMO_PASSWORD",
    "nurse_user": "NURSE_PASSWORD",
}


def main() -> None:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "username TEXT PRIMARY KEY, salt TEXT NOT NULL, password_hash TEXT NOT NULL)"
    )
    for username, env_name in TRAINING_USERS.items():
        password = os.environ.get(env_name)
        if not password:
            print(f"Skipped {username}: set the {env_name} environment variable first")
            continue
        salt_hex, hash_hex = make_password_record(password)
        connection.execute(
            "INSERT OR REPLACE INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
            (username, salt_hex, hash_hex),
        )
        print(f"Saved {username}")
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
