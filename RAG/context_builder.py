"""
Context Builder

Builds a structured context from retrieved document chunks.
The generated context will later be provided to the LLM.
"""

from typing import Any


class ContextBuilder:
    """
    Build a context from retrieved chunks.
    """

    def __init__(self, max_chunks: int = 5):
        """
        Parameters
        ----------
        max_chunks : int
            Maximum number of chunks included in the context.
        """

        self.max_chunks = max_chunks

    def build(
        self,
        retrieved_chunks: list[dict[str, Any]]
    ) -> str:
        """
        Build a structured textual context.

        Parameters
        ----------
        retrieved_chunks : list[dict]
            Chunks returned by the Retriever.

        Returns
        -------
        str
            Structured context for the LLM.
        """

        if not retrieved_chunks:
            return ""

        # Limit the number of chunks
        chunks = retrieved_chunks[:self.max_chunks]

        context_parts = []

        for index, chunk in enumerate(chunks, start=1):

            metadata = chunk.get("metadata", {})

            file_name = metadata.get(
                "file_name",
                "Unknown document"
            )

            chunk_id = metadata.get(
                "chunk_id",
                "Unknown"
            )

            text = chunk.get(
                "text",
                ""
            )

            context_parts.append(
                f"""
==================================================
SOURCE {index}
==================================================

Document : {file_name}
Chunk : {chunk_id}

{text}
"""
            )

        return "\n".join(context_parts)