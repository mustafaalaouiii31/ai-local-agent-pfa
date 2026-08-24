"""
TXT Reader
"""

from pathlib import Path

from models.document import DocumentData
from  Pipline_automatique.Detection.document_detector import DocumentType
from .base_reader import BaseReader


class TxtReader(BaseReader):

    def read(self, file_path: str) -> DocumentData:

        with open(file_path, "r", encoding="utf-8") as file:
            raw_text = file.read()

        return DocumentData(
            file_name=Path(file_path).name,
            file_path=file_path,
            file_type=DocumentType.TEXT.value,
            raw_text=raw_text,
            total_pages=1,
            metadata={}
        )