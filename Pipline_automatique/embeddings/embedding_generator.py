"""
Embedding Generator

Generate embeddings for document chunks using Sentence Transformers.
"""

from functools import lru_cache
from sentence_transformers import SentenceTransformer
from models.document import DocumentData


class EmbeddingGenerator:
    """
    Generate embeddings for document chunks
    and query embeddings.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3"
    ):
        """
        Load the embedding model.
        """

        print(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(
            model_name,
            trust_remote_code=True
        )

        print("Embedding model loaded successfully.")

    def generate(
        self,
        document: DocumentData
    ) -> DocumentData:
        """
        Generate embeddings for all document chunks.
        """

        if not document.chunks:
            raise ValueError(
                "Document contains no chunks."
            )

        texts = [
            chunk.text
            for chunk in document.chunks
        ]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        for chunk, embedding in zip(
            document.chunks,
            embeddings
        ):
            chunk.embedding = embedding.tolist()

        return document

    def generate_query_embedding(
        self,
        text: str
    ) -> list[float]:
        """
        Generate an embedding for a user query.
        """

        if not text or not text.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )

        return embedding.tolist()


@lru_cache(maxsize=1)
def get_embedding_generator(model_name: str = "BAAI/bge-m3") -> EmbeddingGenerator:
    """Reuse one loaded embedding model across ingestion and retrieval."""
    return EmbeddingGenerator(model_name=model_name)
