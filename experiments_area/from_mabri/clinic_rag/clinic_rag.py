from functools import cache
from typing import TypedDict

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-mini"
COLLECTION_NAME = "clinic_docs"
QDRANT_URL = "http://localhost:6333"
TOP_K = 3
RELEVANCE_THRESHOLD = 0.4
NO_ANSWER_MESSAGE = (
    "Sorry, I could not find that in our clinic documents. "
    "Please contact the clinic on 555-0142 and our staff will help you."
)


class ClinicState(TypedDict):
    question: str
    chunks: list[str]
    answer: str


@cache
def get_openai_client() -> OpenAI:
    load_dotenv()
    return OpenAI()


@cache
def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL)


def retrieve(state: ClinicState) -> ClinicState:
    response = get_openai_client().embeddings.create(model=EMBEDDING_MODEL, input=state["question"])
    question_vector = response.data[0].embedding
    hits = get_qdrant_client().query_points(
        collection_name=COLLECTION_NAME,
        query=question_vector,
        limit=TOP_K,
        score_threshold=RELEVANCE_THRESHOLD,
        with_payload=True,
    ).points
    state["chunks"] = [f"[{hit.payload['source']}] {hit.payload['text']}" for hit in hits]
    return state
