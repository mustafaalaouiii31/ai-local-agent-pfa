"""Resolve document references in a user request without database ordering."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path


class DocumentSelector:
    """Select documents from a known list using general user references."""

    @staticmethod
    def _normalise(value: str) -> str:
        value = unicodedata.normalize("NFKD", value)
        value = "".join(char for char in value if not unicodedata.combining(char))
        return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

    def resolve(self, query: str, available_documents: list[str], requested_documents: list[str] | None = None, intent: str = "document_question") -> list[str] | None:
        """Resolve explicit references; never select the first database item."""
        available = list(dict.fromkeys(available_documents))
        allowed = [name for name in (requested_documents or available) if name in available]
        if not allowed:
            return []
        if len(allowed) == 1:
            return allowed

        query_normalised = self._normalise(query)
        matches = []
        for document in allowed:
            full_name = self._normalise(document)
            stem = self._normalise(Path(document).stem)
            stem_words = [word for word in stem.split() if len(word) >= 3]
            if (full_name in query_normalised or stem in query_normalised or
                    (stem_words and all(word in query_normalised.split() for word in stem_words))):
                matches.append(document)
        if matches:
            return list(dict.fromkeys(matches))

        ordinals = ((0, (r"\bpremier\b", r"\b1er\b")), (1, (r"\bdeuxieme\b", r"\bsecond\b", r"\b2eme\b", r"\b2e\b")), (2, (r"\btroisieme\b", r"\b3eme\b", r"\b3e\b")))
        for position, patterns in ordinals:
            if position < len(allowed) and any(re.search(pattern, query_normalised) for pattern in patterns):
                return [allowed[position]]

        if "les deux" in query_normalised and len(allowed) == 2:
            return allowed
        if intent in {"comparison", "recommendation"} and len(allowed) == 2:
            return allowed
        if intent == "summary":
            return []
        return allowed if requested_documents is not None else None
