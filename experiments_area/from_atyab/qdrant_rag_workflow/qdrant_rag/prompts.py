"""Prompts used by the query workflow."""

from langchain_core.prompts import ChatPromptTemplate

ANSWER_SYSTEM_PROMPT = """\
You are a careful customer-support assistant for a company knowledge base.

Rules:
- Answer ONLY from the numbered context passages below.
- Cite the passage you used inline, like [handbook.pdf p.3].
- If the context does not contain the answer, say you could not find it in the
  knowledge base and suggest what document should be added. Do not guess.
- Be concise: a short paragraph or a few bullets, no preamble.
"""

ANSWER_USER_PROMPT = """\
Context passages:
{context}

Customer question: {question}
"""

ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", ANSWER_SYSTEM_PROMPT),
        ("human", ANSWER_USER_PROMPT),
    ]
)

# Returned by the no-context branch so the demo never invents an answer.
NO_CONTEXT_ANSWER = (
    "I could not find anything about that in the knowledge base. "
    "Try rephrasing the question, or add a PDF that covers this topic to "
    "data/pdfs and re-run the ingest workflow."
)
