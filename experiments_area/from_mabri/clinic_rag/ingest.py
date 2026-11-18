import uuid
from functools import cache
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

COLLECTION_NAME = "clinic_docs"
QDRANT_URL = "http://localhost:6333"
EMBEDDING_MODEL = "text-embedding-3-small"
VECTOR_SIZE = 1536
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
PDF_DIR = Path(__file__).parent / "sample_pdfs"


def load_pdf_text(file_path: Path) -> str:
    """Load a PDF file and return its text content."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list:
    """Split text into chunks of specified size with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += chunk_size - overlap
    return chunks


@cache
def get_openai_client() -> OpenAI:
    load_dotenv()
    return OpenAI()


def embed_texts(chunks: list[str]) -> list[list[float]]:
    """Turn each chunk into one embedding vector, in the same order."""
    response = get_openai_client().embeddings.create(model=EMBEDDING_MODEL, input=chunks)
    return [item.embedding for item in response.data]


@cache
def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL)


def store_chunks(chunks: list[str], vectors: list[list[float]], source: str) -> int:
    """Save each chunk and its vector in Qdrant, tagged with the PDF file name."""
    client = get_qdrant_client()
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
    points = [
        PointStruct(
            id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source}#{index}")),
            vector=vector,
            payload={"text": chunk, "source": source},
        )
        for index, (chunk, vector) in enumerate(zip(chunks, vectors, strict=True))
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)


