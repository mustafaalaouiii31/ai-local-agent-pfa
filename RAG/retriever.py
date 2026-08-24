"""
RAG Retriever

Retrieves the most relevant document chunks from ChromaDB
using semantic similarity.
"""

from typing import Any, Optional
import logging
from time import perf_counter

from Pipline_automatique.embeddings.embedding_generator import get_embedding_generator

from Pipline_automatique.indexing.chroma_indexer import (
    ChromaIndexer
)


class Retriever:
    """
    Retrieve relevant document chunks for a user query.
    """

    def __init__(
        self,
        top_k: int = 4
    ):
        """
        Initialize the retriever.

        Parameters
        ----------
        top_k : int
            Number of chunks to retrieve.
        """

        self.top_k = top_k

        # Same embedding model used during ingestion
        self.embedding_generator = get_embedding_generator()

        # ChromaDB interface
        self.indexer = ChromaIndexer()

    # ==================================================
    # RETRIEVE
    # ==================================================

    def retrieve(
        self,
        query: str,
        document_names: Optional[list[str]] = None
    ) -> list[dict[str, Any]]:
        """
        Retrieve the most relevant chunks for a query.

        Parameters
        ----------
        query : str
            User question.

        document_names : list[str] | None
            Optional list of documents to search in.

            If None:
                Search all documents.

            If provided:
                Search only inside these documents.

        Returns
        -------
        list[dict]
            Relevant chunks with metadata and similarity
            information.
        """

        # ---------------------------------
        # 1. Validate query
        # ---------------------------------

        if not query or not query.strip():

            raise ValueError(
                "Query cannot be empty."
            )

        # ---------------------------------
        # 2. Generate query embedding
        # ---------------------------------

        embedding_started = perf_counter()
        query_embedding = (
            self.embedding_generator
            .generate_query_embedding(query)
        )
        logging.getLogger(__name__).info(
            "[PERF] Query embedding: %.3fs", perf_counter() - embedding_started
        )

        # ---------------------------------
        # 3. Search ChromaDB
        # ---------------------------------

        search_started = perf_counter()
        results = self.indexer.search(
            query_embedding=query_embedding,
            top_k=self.top_k,
            document_names=document_names
        )
        logging.getLogger(__name__).info(
            "[PERF] Chroma search: %.3fs", perf_counter() - search_started
        )

        # ---------------------------------
        # 4. Convert ChromaDB result
        # ---------------------------------

        retrieved_chunks = []

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        ids = results.get(
            "ids",
            [[]]
        )[0]

        # ---------------------------------
        # 5. Build retrieved chunks
        # ---------------------------------

        for i in range(
            len(documents)
        ):

            retrieved_chunks.append(
                {
                    "id": ids[i],
                    "text": documents[i],
                    "metadata": metadatas[i],
                    "distance": distances[i],
                }
            )

        return retrieved_chunks
