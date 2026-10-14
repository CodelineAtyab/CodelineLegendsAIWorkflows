# Entry point: runs the interactive chat loop and wires the utils together.

from utils.client import create_client, send_message
from utils.config import EXIT_WORDS, MODEL, require_api_key
from utils.session import load_session, resolve_session_id, save_session


def main():
    # 1. Make sure the API key is available before doing anything else.
    require_api_key()

    # 2. Prepare the client and decide which conversation to continue.
    client = create_client()
    session_id = resolve_session_id()

    # 3. Load any previously saved messages for this session (empty on first run).
    messages = load_session(session_id)
    user_input = ""

    print(f"Chat with {MODEL} — session {session_id}")
    print("(type 'exit' or 'quit' to stop)\n")

    # 4. Loop until the user types an exit word (checked in the condition).
    while user_input.lower() not in EXIT_WORDS:
        user_input = input("You: ").strip()

        # Skip blank input; exit words are handled by the loop condition above.
        if user_input and user_input.lower() not in EXIT_WORDS:
            # Record the user's message, ask the model, then record its reply.
            messages.append({"role": "user", "content": user_input})
            reply = send_message(client, messages)
            messages.append({"role": "assistant", "content": reply})

            # Persist the updated history so it survives the next run.
            save_session(session_id, messages)
            print(f"Assistant: {reply}\n")


if __name__ == "__main__":
    main()
