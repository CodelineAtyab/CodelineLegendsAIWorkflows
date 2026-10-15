import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

#Define constants and load the API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4.1-mini"
BASE_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = BASE_DIR / "sessions"
INDEX_FILE = SESSIONS_DIR / "index.json"

#Create a function to read the index
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

#Create a function to save JSON   
def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return True

    except OSError:
        print("Could not save the file.")
        return False

#Generate a session name using AI 
def generate_name(client, question):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Generate exactly two short English words "
                        "describing the user's question. "
                        "Return only the two words."
                    ),
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )

        text = response.choices[0].message.content or ""
        words = re.findall(r"[a-z]+", text.lower())

        if len(words) >= 2:
            return "_".join(words[:2])

        return "new_session"

    except Exception:
        print("Could not generate session name.")
        return "new_session"
    
#Create the function that asks AI a question
def get_answer(client, messages):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )

        return response.choices[0].message.content or ""

    except Exception:
        print("Could not get an AI response.")
        return None
#Load an old conversation
def load_history(name):
    path = SESSIONS_DIR / f"{name}.json"

    try:
        with open(path, "r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            print("Invalid session history.")
            return None

        return history

    except (OSError, json.JSONDecodeError):
        print("Could not load session history.")
        return None