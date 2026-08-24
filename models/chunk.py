"""
Chunk model.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ChunkData:
    """
    Represents one chunk of a document.
    """

    chunk_id: int

    text: str

    metadata: dict[str, Any] = field(default_factory=dict)

    embedding: list[float] = field(default_factory=list)