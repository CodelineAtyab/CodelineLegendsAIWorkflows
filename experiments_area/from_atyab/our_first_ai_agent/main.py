import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "gpt-4.1-mini"
EXIT_WORDS = {"exit", "quit"}


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Error: OPENAI_API_KEY is not set in your environment.")

    client = OpenAI()
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    user_input = ""

    print("Chat with gpt-4.1-mini (type 'exit' or 'quit' to stop).\n")
    while user_input.lower() not in EXIT_WORDS:
        user_input = input("You: ").strip()

        if user_input and user_input.lower() not in EXIT_WORDS:
            messages.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
            )
            reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            print(f"Assistant: {reply}\n")


if __name__ == "__main__":
    main()
