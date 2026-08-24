"""
Short-Term Memory

Stores the recent conversation context of the agent.
"""

from typing import Any


class ShortTermMemory:
    """
    Stores recent messages and the documents currently
    relevant to the conversation.
    """

    def __init__(
        self,
        max_messages: int = 10
    ):
        self.max_messages = max_messages

        self.messages: list[dict[str, Any]] = []

        self.documents: list[str] = []

        self.active_document: str | None = None

    # ==================================================
    # MESSAGES
    # ==================================================

    def add_message(
        self,
        role: str,
        content: str
    ) -> None:

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

        # Keep only recent messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[
                -self.max_messages:
            ]

    # ==================================================
    # GET MESSAGES
    # ==================================================

    def get_messages(self) -> list[dict[str, Any]]:

        return list(self.messages)

    # ==================================================
    # DOCUMENTS
    # ==================================================

    def set_documents(
        self,
        documents: list[str]
    ) -> None:

        self.documents = list(dict.fromkeys(documents))

    def add_document(
        self,
        document_name: str
    ) -> None:

        if document_name not in self.documents:
            self.documents.append(document_name)

        self.active_document = document_name

    def set_active_document(
        self,
        document_name: str
    ) -> None:

        self.active_document = document_name

        if document_name not in self.documents:
            self.documents.append(document_name)

    def get_documents(self) -> list[str]:

        return list(self.documents)

    def get_active_document(self) -> str | None:

        return self.active_document

    # ==================================================
    # CONTEXT
    # ==================================================

    def get_context(
        self,
        max_messages: int | None = None
    ) -> str:

        messages = self.messages

        if max_messages is not None:
            messages = messages[-max_messages:]

        if not messages and not self.documents:
            return ""

        parts = []

        if self.documents:

            parts.append(
                "DOCUMENTS DISPONIBLES DANS LA CONVERSATION:"
            )

            for document in self.documents:
                parts.append(
                    f"- {document}"
                )

        if self.active_document:

            parts.append(
                f"\nDOCUMENT ACTUEL : {self.active_document}"
            )

        if messages:

            parts.append(
                "\nHISTORIQUE RÉCENT DE LA CONVERSATION:"
            )

            for message in messages:

                role = message["role"]

                content = message["content"]

                if role == "user":
                    label = "Utilisateur"
                else:
                    label = "Agent"

                parts.append(
                    f"{label}: {content}"
                )

        return "\n".join(parts)

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(self) -> None:

        self.messages = []

        self.documents = []

        self.active_document = None