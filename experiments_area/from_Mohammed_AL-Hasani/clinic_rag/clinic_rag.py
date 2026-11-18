"""LangGraph RAG workflow: question -> retrieve chunks -> answer from those chunks.

Run after ingestion:  uv run clinic_rag.py
"""

from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from ingest import COLLECTION_NAME, embed_texts, openai_client, qdrant_client

ANSWER_MODEL = "gpt-4.1-mini"
TOP_K = 3
MIN_SCORE = 0.35  # chunks less similar than this are treated as "not found"
NO_ANSWER_MESSAGE = (
    "Sorry, I could not find that in our clinic information. "
    "Please contact the clinic directly on 5550-0123."
)
SYSTEM_PROMPT = (
    "You are the clinic booking assistant. Answer the customer's question using ONLY the "
    "clinic information below. If it does not contain the answer, say you do not know. "
    "Keep the answer short.\n\nClinic information:\n{context}"
)
TEST_QUESTIONS = [
    "What time do you open on Friday?",
    "Do you accept walk-ins?",
    "How do I cancel an appointment?",
    "How much is a dental check-up?",
    "Is there a fee if I cancel late?",
    "Do you sell car insurance?",
]


class ClinicState(TypedDict):
    question: str
    chunks: list[str]
    answer: str


def retrieve(state: ClinicState) -> ClinicState:
    """Embed the question and keep the most similar chunks found in Qdrant."""
    question_vector = embed_texts([state["question"]])[0]
    result = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_vector,
        limit=TOP_K,
        score_threshold=MIN_SCORE,
    )
    state["chunks"] = [point.payload["text"] for point in result.points if point.payload]
    return state


def generate(state: ClinicState) -> ClinicState:
    """Ask the model to answer from the retrieved chunks only."""
    context = "\n\n".join(state["chunks"])
    response = openai_client.chat.completions.create(
        model=ANSWER_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
            {"role": "user", "content": state["question"]},
        ],
    )
    state["answer"] = response.choices[0].message.content or ""
    return state


def no_answer(state: ClinicState) -> ClinicState:
    """Polite fallback when nothing relevant was retrieved."""
    state["answer"] = NO_ANSWER_MESSAGE
    return state


def decide_next_step(state: ClinicState) -> str:
    """Answer when at least one chunk was found, otherwise fall back."""
    if state["chunks"]:
        return "generate"
    return "no_answer"


graph = StateGraph(ClinicState)

graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.add_node("no_answer", no_answer)

graph.add_edge(START, "retrieve")
graph.add_conditional_edges(
    "retrieve", decide_next_step, {"generate": "generate", "no_answer": "no_answer"}
)
graph.add_edge("generate", END)
graph.add_edge("no_answer", END)

workflow = graph.compile()


def main() -> None:
    diagram_path = Path(__file__).with_suffix(".png")
    diagram_path.write_bytes(workflow.get_graph().draw_mermaid_png())
    print(f"Graph saved to {diagram_path}")

    for question in TEST_QUESTIONS:
        print(workflow.invoke({"question": question, "chunks": [], "answer": ""}))


if __name__ == "__main__":
    main()
