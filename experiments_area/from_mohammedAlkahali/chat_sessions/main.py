import json
from dotenv import load_dotenv 
from openai import OpenAI

load_dotenv()

def save_session(file_name, messages):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4)

def load_session(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def main():
    client = OpenAI()
    message = load_session("chat_session.json")

    while True:
        user_input = input("You: ")

        if user_input in ["exit", "EXIT"]:
            break

        message.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=message,
        )
        reply = response.choices[0].message.content

        print("bot:", reply)
        message.append({"role": "assistant", "content": reply})
        save_session("chat_session.json", message)
        

if __name__ == "__main__":
    main()