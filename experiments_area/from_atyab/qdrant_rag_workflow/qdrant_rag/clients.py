"""Lazily created clients.

Nothing here talks to the network at import time or while a graph is being
compiled, which is what lets `main.py graphs` render the workflow diagrams
without Docker or an OpenAI key running.
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from pydantic import SecretStr
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, VectorParams

from qdrant_rag.config import Settings


def build_qdrant_client(settings: Settings) -> QdrantClient:
    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        timeout=30,
        # Skip the background version handshake: the demo pins the image version
        # in docker-compose.yml, and a missing server should not print a warning
        # while graphs are being compiled.
        check_compatibility=False,
    )


def build_embeddings(settings: Settings) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        dimensions=settings.embedding_dimensions,
        api_key=SecretStr(settings.require_openai_key()),
        # Keep embedding requests comfortably below the per-request token cap.
        chunk_size=64,
    )


def build_chat_model(settings: Settings) -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.chat_model,
        temperature=0,
        api_key=SecretStr(settings.require_openai_key()),
    )


def collection_vector_size(client: QdrantClient, name: str) -> int | None:
    """Vector size of an existing collection, or None when it cannot be read."""
    vectors = client.get_collection(name).config.params.vectors
    if isinstance(vectors, dict):  # named vectors are not used by this project
        first = next(iter(vectors.values()), None)
        return None if first is None else first.size
    return None if vectors is None else vectors.size


class WorkflowDeps:
    """Per-run cache of the expensive-to-build clients.

    These are methods, not properties, on purpose: when a graph is compiled,
    LangGraph introspects every attribute path a node function loads and calls
    `getattr` on it. A property would be executed at compile time, which would
    create clients (and hit the network) before the workflow even runs.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client: QdrantClient | None = None
        self._embeddings: OpenAIEmbeddings | None = None
        self._store: QdrantVectorStore | None = None
        self._chat: ChatOpenAI | None = None

    def client(self) -> QdrantClient:
        if self._client is None:
            self._client = build_qdrant_client(self.settings)
        return self._client

    def embeddings(self) -> OpenAIEmbeddings:
        if self._embeddings is None:
            self._embeddings = build_embeddings(self.settings)
        return self._embeddings

    def store(self) -> QdrantVectorStore:
        if self._store is None:
            self._store = QdrantVectorStore(
                client=self.client(),
                collection_name=self.settings.collection_name,
                embedding=self.embeddings(),
            )
        return self._store

    def chat(self) -> ChatOpenAI:
        if self._chat is None:
            self._chat = build_chat_model(self.settings)
        return self._chat

    def ensure_collection(self, *, recreate: bool = False) -> None:
        """Create the collection (or reset it) with the expected vector size."""
        name = self.settings.collection_name
        size = self.settings.embedding_dimensions
        client = self.client()

        if recreate and client.collection_exists(name):
            client.delete_collection(name)
            print(f"  dropped collection {name!r}")

        if not client.collection_exists(name):
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE),
            )
            print(f"  created collection {name!r} (size={size}, distance=cosine)")
            return

        existing_size = collection_vector_size(client, name)
        if existing_size is not None and existing_size != size:
            raise RuntimeError(
                f"Collection {name!r} stores {existing_size}-dim vectors but "
                f"{self.settings.embedding_model} produces {size}. "
                "Re-run with --recreate to rebuild it."
            )

    def ping(self) -> None:
        """Fail fast with a helpful message when Qdrant is not reachable."""
        try:
            self.client().get_collections()
        except UnexpectedResponse as error:
            raise RuntimeError(
                f"Qdrant answered with an error at {self.settings.qdrant_url}. "
                "Check QDRANT_URL and QDRANT_API_KEY."
            ) from error
        except Exception as error:  # noqa: BLE001 - network errors vary by client
            raise RuntimeError(
                f"Cannot reach Qdrant at {self.settings.qdrant_url}. "
                "Start it first:\n"
                "  docker compose -f docker/docker-compose.yml up -d"
            ) from error
