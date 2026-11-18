from functools import cache
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
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
SYSTEM_PROMPT = (
    "You are the booking assistant of Sunrise Family Clinic. "
    "Answer the customer's question using only the clinic documents you are given. "
    "Keep the answer short and friendly. "
    f"If the documents do not contain the answer, reply exactly: {NO_ANSWER_MESSAGE}"
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


def decide_next_step(state: ClinicState) -> str:
    if state["chunks"]:
        return "generate"
    return "no_answer"


def generate(state: ClinicState) -> ClinicState:
    documents = "\n\n".join(state["chunks"])
    response = get_openai_client().chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Clinic documents:\n{documents}\n\nCustomer question: {state['question']}"},
        ],
    )
    state["answer"] = response.choices[0].message.content
    return state


def no_answer(state: ClinicState) -> ClinicState:
    state["answer"] = NO_ANSWER_MESSAGE
    return state


graph = StateGraph(ClinicState)

graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.add_node("no_answer", no_answer)

graph.add_edge(START, "retrieve")
graph.add_conditional_edges("retrieve", decide_next_step, {"generate": "generate", "no_answer": "no_answer"})
graph.add_edge("generate", END)
graph.add_edge("no_answer", END)

workflow = graph.compile()
