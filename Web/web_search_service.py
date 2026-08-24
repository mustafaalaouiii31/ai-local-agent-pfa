"""Web-search fallback boundary.

This component intentionally does not call an external API yet.  It only
decides whether the UI should offer an opt-in Web search, keeping Web logic
separate from the local RAG, ChromaDB and Retriever components.
"""


class WebSearchService:
    """Prepare an optional Web search without executing one automatically."""

    _RECENCY_CUES = (
        "aujourd", "actuel", "derniere", "dernier", "recent", "2026",
        "prix", "cours", "news", "actualité", "actualite",
    )
    _UNCERTAINTY_CUES = (
        "je ne sais pas", "je n'ai pas assez", "je ne peux pas confirmer",
        "information incertaine", "a verifier", "à vérifier", "pas certain",
        "information non disponible", "je ne dispose pas", "je n'ai pas pu",
        "je ne peux pas repondre", "je ne peux pas répondre", "je ne connais pas",
    )

    def should_offer(self, query: str, answer: str = "") -> bool:
        """Return True only when fresh/external information is likely useful."""
        query_normalized = query.lower()
        answer_normalized = answer.lower()
        return (
            any(cue in query_normalized for cue in self._RECENCY_CUES)
            or any(cue in answer_normalized for cue in self._UNCERTAINTY_CUES)
        )

    @staticmethod
    def unavailable_message() -> str:
        """Temporary response until a chosen Web provider is configured."""
        return "La recherche Web n’est pas encore connectée. Aucun appel externe n’a été effectué."
