# Session storage: each conversation is saved to its own JSON file so it can be
# resumed on a later run. Files live in SESSIONS_DIR and are named "<session_id>.json".

import json
import os
import sys
from uuid import uuid4

from .config import SESSIONS_DIR


def session_file(session_id: str) -> str:
    """Build the filesystem path (as a string) for a session's history file."""
    return os.path.join(SESSIONS_DIR, f"{session_id}.json")


def load_session(session_id: str) -> list:
    """Return the saved message list for a session, or [] if none exists yet."""
    path = session_file(session_id)

    # 1. Nothing saved for this session -> start a brand new conversation.
    if not os.path.exists(path):
        return []

    # 2. Read and parse the JSON array of messages stored on disk.
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # 3. Only accept the expected shape; anything else is treated as empty.
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError):
        # 4. Corrupt or unreadable file -> warn and start fresh instead of crashing.
        print(f"Warning: could not read {os.path.basename(path)}, starting fresh.\n")

    return []


def save_session(session_id: str, messages: list) -> None:
    """Write the full message list for a session to disk."""
    # 1. Ensure the sessions directory exists before writing into it.
    os.makedirs(SESSIONS_DIR, exist_ok=True)

    # 2. Overwrite the session file with the complete, pretty-printed history.
    with open(session_file(session_id), "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=2, ensure_ascii=False)


def resolve_session_id() -> str:
    """Pick which session to use: explicit CLI arg, else most recent, else new."""
    # 1. An explicit id passed on the command line always takes priority.
    if len(sys.argv) > 1:
        return sys.argv[1]

    # 2. Otherwise resume the most recently modified session file, if any.
    if SESSIONS_DIR.exists():
        sessions = sorted(
            SESSIONS_DIR.glob("*.json"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        if sessions:
            return sessions[0].stem

    # 3. No saved sessions -> generate a new unique id.
    return str(uuid4())
