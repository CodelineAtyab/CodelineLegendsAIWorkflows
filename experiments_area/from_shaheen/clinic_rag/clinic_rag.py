from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from openai import OpenAI
from qdrant_client import QdrantClient

# Must be the same embedding model that ingest.py used to store the chunks.
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-mini"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "clinic_docs"
TOP_K = 3
# Cosine similarity below this means the chunk is not about the question.
SCORE_THRESHOLD = 0.3

ANSWER_INSTRUCTIONS = (
    "You are the booking assistant of a clinic. Answer the customer's question using only "
    "the clinic information below. If the answer is not in that information, say that you "
    "do not know and ask the customer to contact the clinic."
)
NO_ANSWER_MESSAGE = (
    "Sorry, I could not find this in the clinic's information. "
    "Please contact the clinic on 555-0142 and our staff will help you."
)
TEST_QUESTIONS = [
    "What time do you open on Friday?",
    "Do you accept walk-ins?",
    "How do I cancel an appointment?",
    "How much does a dental cleaning cost?",
    "Do you sell car insurance?",
]

# OpenAI() reads OPENAI_API_KEY from the environment, which load_dotenv fills from .env.
load_dotenv()
openai_client = OpenAI()
qdrant_client = QdrantClient(url=QDRANT_URL)


class ClinicState(TypedDict):
    question: str
    chunks: list[str]
    answer: str


def retrieve(state: ClinicState) -> ClinicState:
    """Embed the question and keep the top matching chunks from Qdrant."""
    response = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=[state["question"]])
    question_vector = response.data[0].embedding

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_vector,
        limit=TOP_K,
        score_threshold=SCORE_THRESHOLD,
    )

    chunks = []
    for point in results.points:
        if point.payload is not None:
            chunks.append(point.payload["text"])
    state["chunks"] = chunks
    return state


def generate(state: ClinicState) -> ClinicState:
    """Ask the chat model to answer the question from the retrieved chunks only."""
    clinic_information = "\n\n".join(state["chunks"])
    response = openai_client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": f"{ANSWER_INSTRUCTIONS}\n\n{clinic_information}"},
            {"role": "user", "content": state["question"]},
        ],
    )
    state["answer"] = response.choices[0].message.content or ""
    return state


def no_answer(state: ClinicState) -> ClinicState:
    """Return a polite message when no chunk matched the question."""
    state["answer"] = NO_ANSWER_MESSAGE
    return state


def decide_next_node(state: ClinicState) -> str:
    """Go to generate when at least one chunk was found, otherwise to no_answer."""
    if state["chunks"]:
        return "generate"
    return "no_answer"


graph = StateGraph(ClinicState)

graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.add_node("no_answer", no_answer)

graph.add_edge(START, "retrieve")
graph.add_conditional_edges(
    "retrieve",
    decide_next_node,
    {"generate": "generate", "no_answer": "no_answer"},
)
graph.add_edge("generate", END)
graph.add_edge("no_answer", END)

workflow = graph.compile()


def main() -> None:
    png_path = Path(__file__).with_suffix(".png")
    png_path.write_bytes(workflow.get_graph().draw_mermaid_png())
    print(f"Graph saved to {png_path.name}\n")

    for question in TEST_QUESTIONS:
        print(workflow.invoke({"question": question, "chunks": [], "answer": ""}))
        print()


if __name__ == "__main__":
    main()
