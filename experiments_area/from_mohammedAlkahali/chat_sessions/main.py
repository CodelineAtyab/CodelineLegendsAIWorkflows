from dotenv import load_dotenv 
from openai import OpenAI

load_dotenv()

def main():
    client = OpenAI()
    message = []

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

if __name__ == "__main__":
    main()