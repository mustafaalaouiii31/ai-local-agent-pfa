"""
Word Reader
"""

from pathlib import Path
from docx import Document

from models.document import DocumentData
from Pipline_automatique.Detection.document_detector import DocumentType
from .base_reader import BaseReader


class WordReader(BaseReader):

    def read(self, file_path: str) -> DocumentData:

        doc = Document(file_path)

        paragraphs = []

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        raw_text = "\n".join(paragraphs)

        metadata = {
            "author": doc.core_properties.author,
            "title": doc.core_properties.title,
            "subject": doc.core_properties.subject,
            "created": str(doc.core_properties.created),
            "modified": str(doc.core_properties.modified),
        }

        return DocumentData(
            file_name=Path(file_path).name,
            file_path=file_path,
            file_type=DocumentType.WORD.value,
            raw_text=raw_text,
            total_pages=0,
            metadata=metadata
        )