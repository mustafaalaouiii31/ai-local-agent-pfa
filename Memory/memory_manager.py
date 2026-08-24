"""
Memory Manager

Central manager for short-term, long-term and
procedural memory.
"""

from .short_term_memory import ShortTermMemory
from .long_term_memory import LongTermMemory
from .procedural_memory import ProceduralMemory


class MemoryManager:

    def __init__(
        self,
        max_short_term_messages: int = 10
    ):

        self.short_term = ShortTermMemory(
            max_messages=max_short_term_messages
        )

        self.long_term = LongTermMemory()

        self.procedural = ProceduralMemory()

    # ==================================================
    # CONVERSATION
    # ==================================================

    def add_message(
        self,
        role: str,
        content: str
    ) -> None:

        self.short_term.add_message(
            role,
            content
        )

    # ==================================================
    # DOCUMENTS
    # ==================================================

    def add_document(
        self,
        document_name: str
    ) -> None:

        self.short_term.add_document(
            document_name
        )

        self.long_term.remember(
            content=f"Document chargé : {document_name}",
            memory_type="document",
            metadata={
                "file_name": document_name
            }
        )

    def set_documents(
        self,
        documents: list[str]
    ) -> None:

        self.short_term.set_documents(
            documents
        )

    def set_active_document(
        self,
        document_name: str
    ) -> None:

        self.short_term.set_active_document(
            document_name
        )

    def get_documents(self) -> list[str]:

        return self.short_term.get_documents()

    def get_active_document(self) -> str | None:

        return self.short_term.get_active_document()

    # ==================================================
    # LONG TERM
    # ==================================================

    def remember(
        self,
        content: str,
        memory_type: str = "general",
        metadata: dict | None = None
    ) -> None:

        self.long_term.remember(
            content,
            memory_type,
            metadata
        )

    # ==================================================
    # CONTEXT
    # ==================================================

    def get_context(self) -> str:

        parts = []

        short_context = (
            self.short_term.get_context()
        )

        if short_context:

            parts.append(
                short_context
            )

        procedural_context = (
            self.procedural.get_context()
        )

        if procedural_context:

            parts.append(
                procedural_context
            )

        return "\n\n".join(parts)

    # ==================================================
    # PROCEDURAL
    # ==================================================

    def get_rules(self) -> list[str]:

        return self.procedural.get_rules()

    def get_procedural_context(self) -> str:

        return self.procedural.get_context()

    # ==================================================
    # CLEAR
    # ==================================================

    def clear_short_term(self) -> None:

        self.short_term.clear()

    # ==================================================
    # FULL RESET
    # ==================================================

    def clear_all(self) -> None:

        self.short_term.clear()

        self.long_term.clear()