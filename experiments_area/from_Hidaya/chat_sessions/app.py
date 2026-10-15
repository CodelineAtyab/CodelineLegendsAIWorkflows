import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4.1-mini"

BASE_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = BASE_DIR / "sessions"
INDEX_FILE = SESSIONS_DIR / "index.json"

def load_index():
    if not INDEX_FILE.exists():
        return {}

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print("Invalid session index.")
            return None

        return data

    except (OSError, json.JSONDecodeError):
        print("Could not read session index.")
        return None