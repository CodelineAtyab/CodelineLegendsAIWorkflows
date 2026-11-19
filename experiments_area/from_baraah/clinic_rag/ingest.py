import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from qdrant_client import QdrantClient, models

load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_SIZE = 1536
COLLECTION_NAME = "clinic_docs"
QDRANT_URL = "http://localhost:6333"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
PDF_FOLDER = Path(__file__).parent / "pdfs"


# Read the text from one PDF.
def load_pdf_text(path: Path) -> str:
    reader = PdfReader(path)
    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages)


# Split text into overlapping chunks.
def split_into_chunks(
    text: str,
    chunk_size: int,
    overlap: int,
) -> list[str]:
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("Invalid chunk size or overlap")

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(text), step):
        chunk = text[start : start + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

        if start + chunk_size >= len(text):
            break

    return chunks


# Convert text chunks into OpenAI embeddings.
def embed_texts(chunks: list[str]) -> list[list[float]]:
    if not chunks:
        return []

    client = OpenAI()

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=chunks,
    )

    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]


# Save chunks and vectors in Qdrant.
def store_chunks(
    chunks: list[str],
    vectors: list[list[float]],
    source: str,
) -> None:
    if len(chunks) != len(vectors):
        raise ValueError("Chunks and vectors must have equal lengths")

    if not chunks:
        return

    client = QdrantClient(url=QDRANT_URL)

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=EMBEDDING_SIZE,
                distance=models.Distance.COSINE,
            ),
        )

    points = []

    for index, (chunk, vector) in enumerate(zip(chunks, vectors)):
        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{source}:{index}",
            )
        )

        point = models.PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "text": chunk,
                "source": source,
            },
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True,
    )


# Run ingestion for every PDF.
def main() -> None:
    pdf_files = sorted(PDF_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing")

    for pdf_path in pdf_files:
        text = load_pdf_text(pdf_path)

        chunks = split_into_chunks(
            text,
            CHUNK_SIZE,
            CHUNK_OVERLAP,
        )

        if not chunks:
            print(f"{pdf_path.name}: no readable text")
            continue

        vectors = embed_texts(chunks)

        store_chunks(
            chunks,
            vectors,
            pdf_path.name,
        )

        print(f"{pdf_path.name}: {len(chunks)} chunks stored")


if __name__ == "__main__":
    main()
