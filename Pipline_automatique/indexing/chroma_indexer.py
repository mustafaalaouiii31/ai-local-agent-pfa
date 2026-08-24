"""
ChromaDB Indexer

Store and retrieve document chunks from ChromaDB.
"""

from typing import List

import chromadb

from models.document import DocumentData


class ChromaIndexer:
    """
    Manage all interactions with ChromaDB.
    """

    def __init__(
        self,
        db_path: str = "database/chroma",
        collection_name: str = "decision_documents",
    ):

        self.client = chromadb.PersistentClient(
            path=db_path
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    # ==================================================
    # STORE
    # ==================================================

    def store(
        self,
        document: DocumentData
    ) -> None:
        """
        Store all chunks of one document.
        """

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in document.chunks:

            chunk_id = (
                f"{document.file_name}_{chunk.chunk_id}"
            )

            ids.append(
                chunk_id
            )

            documents.append(
                chunk.text
            )

            embeddings.append(
                chunk.embedding
            )

            metadata = dict(
                chunk.metadata or {}
            )

            # Ensure document name is always available
            metadata["file_name"] = (
                document.file_name
            )

            metadata["chunk_id"] = (
                chunk.chunk_id
            )

            metadatas.append(
                metadata
            )

        if not ids:
            return

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    # ==================================================
    # SEARCH
    # ==================================================

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        document_names: list[str] | None = None,
    ):
        """
        Search similar chunks.

        If document_names are provided,
        search only inside those documents.
        """

        kwargs = {
            "query_embeddings": [
                query_embedding
            ],
            "n_results": top_k,
        }

        # ==================================================
        # DOCUMENT FILTER
        # ==================================================

        if document_names:

            clean_names = [
                name
                for name in document_names
                if name
            ]

            if len(clean_names) == 1:

                kwargs["where"] = {
                    "file_name": clean_names[0]
                }

            elif len(clean_names) > 1:

                kwargs["where"] = {
                    "$or": [
                        {
                            "file_name": name
                        }
                        for name in clean_names
                    ]
                }

        return self.collection.query(
            **kwargs
        )

    # ==================================================
    # GET ALL CHUNKS OF A DOCUMENT
    # ==================================================

    def get_document_chunks(
        self,
        document_name: str
    ) -> list[dict]:
        """
        Retrieve all chunks belonging to one document.

        Parameters
        ----------
        document_name : str
            Exact document name.

        Returns
        -------
        list[dict]
            All chunks ordered by chunk_id.
        """

        if not document_name:

            return []

        results = self.collection.get(
            where={
                "file_name": document_name
            }
        )

        documents = results.get(
            "documents",
            []
        )

        metadatas = results.get(
            "metadatas",
            []
        )

        ids = results.get(
            "ids",
            []
        )

        chunks = []

        for chunk_id, text, metadata in zip(
            ids,
            documents,
            metadatas
        ):

            metadata = metadata or {}

            chunks.append(
                {
                    "id": chunk_id,
                    "text": text,
                    "metadata": metadata
                }
            )

        # ==================================================
        # SORT BY CHUNK ID
        # ==================================================

        def chunk_sort_key(chunk):

            value = chunk["metadata"].get(
                "chunk_id",
                0
            )

            try:
                return int(value)

            except (
                ValueError,
                TypeError
            ):
                return 0

        chunks.sort(
            key=chunk_sort_key
        )

        return chunks

    # ==================================================
    # GET DOCUMENT NAMES
    # ==================================================

    def get_document_names(
        self
    ) -> list[str]:
        """
        Return unique document names stored in ChromaDB.
        """

        results = self.collection.get()

        metadatas = results.get(
            "metadatas",
            []
        )

        names = []

        for metadata in metadatas:

            if not metadata:
                continue

            file_name = metadata.get(
                "file_name"
            )

            if not file_name:
                continue

            if file_name not in names:

                names.append(
                    file_name
                )

        return names

    # ==================================================
    # GET DOCUMENT SUMMARIES
    # ==================================================

    def get_document_summaries(
        self
    ) -> list[dict]:
        """
        Return information about stored documents.

        Used by the Streamlit interface.
        """

        results = self.collection.get()

        ids = results.get(
            "ids",
            []
        )

        metadatas = results.get(
            "metadatas",
            []
        )

        documents = results.get(
            "documents",
            []
        )

        document_data = {}

        for index, metadata in enumerate(
            metadatas
        ):

            if not metadata:
                continue

            file_name = metadata.get(
                "file_name"
            )

            if not file_name:
                continue

            if file_name not in document_data:

                document_data[file_name] = {
                    "name": file_name,
                    "chunks": 0
                }

            document_data[file_name]["chunks"] += 1

        return list(
            document_data.values()
        )

    # ==================================================
    # DOCUMENT EXISTS
    # ==================================================

    def document_exists(
        self,
        document_name: str
    ) -> bool:
        """
        Check whether a document exists.
        """

        if not document_name:
            return False

        results = self.collection.get(
            where={
                "file_name": document_name
            },
            limit=1
        )

        return bool(
            results.get(
                "ids",
                []
            )
        )

    # ==================================================
    # DELETE DOCUMENT
    # ==================================================

    def delete_document(
        self,
        document_name: str,
    ) -> None:
        """
        Delete all chunks belonging to one document.
        """

        if not document_name:
            return

        results = self.collection.get(
            where={
                "file_name": document_name
            }
        )

        ids = results.get(
            "ids",
            []
        )

        if ids:

            self.collection.delete(
                ids=ids
            )

    # ==================================================
    # COUNT
    # ==================================================

    def count(
        self
    ) -> int:
        """
        Return number of stored chunks.
        """

        return self.collection.count()

    # ==================================================
    # RESET
    # ==================================================

    def reset(
        self
    ) -> None:
        """
        Delete every stored chunk.
        """

        collection_name = (
            self.collection.name
        )

        self.client.delete_collection(
            collection_name
        )

        self.collection = (
            self.client.get_or_create_collection(
                collection_name
            )
        )