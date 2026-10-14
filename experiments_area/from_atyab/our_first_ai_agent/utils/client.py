# All OpenAI interaction lives here: creating the client, shaping the request,
# and extracting the reply text.

from openai import OpenAI

from .config import MAX_HISTORY_MESSAGES, MODEL, SYSTEM_PROMPT


def create_client() -> OpenAI:
    """Create the OpenAI client (reads OPENAI_API_KEY from the environment)."""
    return OpenAI()


def build_payload(messages: list) -> list:
    """System prompt + the most recent messages, to bound context size."""
    return [SYSTEM_PROMPT] + messages[-MAX_HISTORY_MESSAGES:]


def send_message(client: OpenAI, messages: list) -> str:
    """Send the trimmed history to the model and return its reply text."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=build_payload(messages),
    )
    return response.choices[0].message.content
