import uuid
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

PDF_FOLDER = Path(__file__).parent / "pdfs"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_SIZE = 1536
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "clinic_docs"

# OpenAI() reads OPENAI_API_KEY from the environment, which load_dotenv fills from .env.
load_dotenv()
openai_client = OpenAI()
qdrant_client = QdrantClient(url=QDRANT_URL)


def load_pdf_text(path: Path) -> str:
    """Return the text of all pages of a PDF as one string."""
    reader = PdfReader(path)
    page_texts = []
    for page in reader.pages:
        page_texts.append(page.extract_text())
    return "\n".join(page_texts)


def split_into_chunks(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Cut the text into chunks of chunk_size characters.

    Each chunk starts with the last `overlap` characters of the previous one.
    """
    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(text), step):
        chunks.append(text[start : start + chunk_size])
        # This chunk already reached the end of the text, so stop here.
        if start + chunk_size >= len(text):
            break
    return chunks


def embed_texts(chunks: list[str]) -> list[list[float]]:
    """Return one embedding vector per chunk, in the same order."""
    response = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=chunks)
    vectors = []
    for item in response.data:
        vectors.append(item.embedding)
    return vectors


def store_chunks(chunks: list[str], vectors: list[list[float]], source: str) -> None:
    """Save each chunk and its vector as a point, with the text and file name as payload."""
    points = []
    for chunk, vector in zip(chunks, vectors):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": chunk, "source": source},
            )
        )
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)


def main() -> None:
    # Start from an empty collection, so running the script again does not store duplicates.
    if qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.delete_collection(COLLECTION_NAME)
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
    )

    for pdf_path in sorted(PDF_FOLDER.glob("*.pdf")):
        text = load_pdf_text(pdf_path)
        chunks = split_into_chunks(text, CHUNK_SIZE, CHUNK_OVERLAP)
        vectors = embed_texts(chunks)
        store_chunks(chunks, vectors, pdf_path.name)
        print(f"{pdf_path.name}: {len(chunks)} chunks stored")


if __name__ == "__main__":
    main()
