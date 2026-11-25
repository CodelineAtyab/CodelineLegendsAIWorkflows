import asyncio
from pathlib import Path
from typing import NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph

from github_tools import get_open_issues, get_recent_commits

REPO_OWNER = "CodelineAtyab"
REPO_NAME = "CodelineLegendsAIWorkflows"
HELP_MESSAGE = "Ask me about issues or commits."
QUESTIONS = [
    "Show open issues",
    "What are the latest commits?",
    "Any new issue today?",
    "Hello",
]


class RepoState(TypedDict):
    question: str
    kind: NotRequired[str]
    answer: NotRequired[str | list[str]]


def classify(state: RepoState) -> dict:
    question = state["question"].lower()
    if "issue" in question:
        return {"kind": "issues"}
    if "commit" in question:
        return {"kind": "commits"}
    return {"kind": "help"}


def route_by_kind(state: RepoState) -> str:
    return state["kind"]


def show_issues(state: RepoState) -> dict:
    issues = asyncio.run(get_open_issues(REPO_OWNER, REPO_NAME))
    return {"answer": issues}


def show_commits(state: RepoState) -> dict:
    commits = asyncio.run(get_recent_commits(REPO_OWNER, REPO_NAME))
    return {"answer": commits}


def help_reply(state: RepoState) -> dict:
    return {"answer": HELP_MESSAGE}


graph = StateGraph(RepoState)
graph.add_node("classify", classify)
graph.add_node("show_issues", show_issues)
graph.add_node("show_commits", show_commits)
graph.add_node("help_reply", help_reply)

graph.add_edge(START, "classify")
graph.add_conditional_edges(
    "classify",
    route_by_kind,
    {
        "issues": "show_issues",
        "commits": "show_commits",
        "help": "help_reply",
    },
)
graph.add_edge("show_issues", END)
graph.add_edge("show_commits", END)
graph.add_edge("help_reply", END)

workflow = graph.compile()


if __name__ == "__main__":
    diagram_path = Path(__file__).with_suffix(".png")
    diagram_path.write_bytes(workflow.get_graph().draw_mermaid_png())
    print(f"Graph saved to {diagram_path.name}")

    for question in QUESTIONS:
        print(workflow.invoke({"question": question}))
