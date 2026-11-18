"""Ingestion: read the clinic PDFs, split them into chunks, embed them and store them in Qdrant.

Run once before asking questions:  uv run ingest.py
"""

import uuid
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

load_dotenv()

PDF_FOLDER = Path(__file__).parent / "sample_pdfs"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "clinic_docs"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_SIZE = 1536  # length of one text-embedding-3-small vector
CHUNK_SIZE = 300
CHUNK_OVERLAP = 60

openai_client = OpenAI()
qdrant_client = QdrantClient(url=QDRANT_URL)


def load_pdf_text(path: Path) -> str:
    """Return all the text of a PDF, page after page."""
    reader = PdfReader(path)
    return "\n".join(page.extract_text() for page in reader.pages)


def split_into_chunks(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Cut the text into chunks of chunk_size characters; each chunk repeats the last
    `overlap` characters of the previous one so a sentence cut in half is not lost."""
    step = chunk_size - overlap
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        if start + chunk_size >= len(text):
            break
        start += step
    return chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Return one vector per text. The question at answer time uses this same function,
    so questions and chunks are always embedded with the same model."""
    response = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def store_chunks(chunks: list[str], vectors: list[list[float]], source: str) -> None:
    """Save each chunk and its vector in Qdrant, with the chunk text and PDF name as payload."""
    points = [
        PointStruct(
            # Same PDF and position always give the same id, so re-running updates points
            # instead of duplicating them.
            id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source}:{position}")),
            vector=vector,
            payload={"text": chunk, "source": source},
        )
        for position, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)


def reset_collection() -> None:
    """Start from an empty collection so removed or edited PDFs leave nothing stale behind."""
    if qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.delete_collection(COLLECTION_NAME)
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
    )


def main() -> None:
    reset_collection()
    for pdf_path in sorted(PDF_FOLDER.glob("*.pdf")):
        text = load_pdf_text(pdf_path)
        chunks = split_into_chunks(text, CHUNK_SIZE, CHUNK_OVERLAP)
        vectors = embed_texts(chunks)
        store_chunks(chunks, vectors, pdf_path.name)
        print(f"{pdf_path.name}: {len(chunks)} chunks stored")


if __name__ == "__main__":
    main()
