"""
Document model used throughout the application.

This object travels across the entire ingestion pipeline.
Each module enriches it with new information.
"""

from dataclasses import dataclass, field
from typing import Any
from models.chunk import ChunkData

@dataclass
class DocumentData:
    """
    Represents a document during the ingestion pipeline.
    """

    # ========= Basic Information ========= #

    file_name: str
    file_path: str
    file_type: str

    # ========= Extracted Content ========= #

    raw_text: str = ""
    cleaned_text: str = ""

    # ========= Document Information ========= #

    total_pages: int = 0

    metadata: dict[str, Any] = field(default_factory=dict)

    # ========= Pipeline Results ========= #

    chunks: list[ChunkData] = field(default_factory=list)
    embeddings: list = field(default_factory=list)