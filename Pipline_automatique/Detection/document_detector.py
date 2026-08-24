"""
Detect the document type.
"""

from enum import Enum
from pathlib import Path

from .file_validator import FileValidator


class DocumentType(Enum):

    PDF = "pdf"

    WORD = "docx"

    EXCEL = "xlsx"

    POWERPOINT = "pptx"

    TEXT = "txt"


class DocumentDetector:

    EXTENSION_MAPPING = {
        ".pdf": DocumentType.PDF,
        ".docx": DocumentType.WORD,
        ".xlsx": DocumentType.EXCEL,
        ".pptx": DocumentType.POWERPOINT,
        ".txt": DocumentType.TEXT,
    }

    @classmethod
    def detect(cls, file_path: str) -> DocumentType:

        FileValidator.validate(file_path)

        extension = Path(file_path).suffix.lower()

        return cls.EXTENSION_MAPPING[extension]