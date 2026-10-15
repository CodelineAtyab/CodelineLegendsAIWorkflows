from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def main():
    user_input = ""
    while user_input not in ["exit", "EXIT"]:
        user_input = input("What do you want to ask ? (or type exit): ")

        if user_input not in ["exit", "EXIT"]:
            client = OpenAI()

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=user_input,
            )

            print(response.output_text)


if __name__ == "__main__":
    main()
