"""
Factory responsible for creating the appropriate reader.
"""

from Pipline_automatique.Detection.document_detector import DocumentType

from .pdf_reader import PDFReader
from .word_reader import WordReader
from .excel_reader import ExcelReader
from .ppt_reader import PPTReader
from .txt_reader import TxtReader


class ReaderFactory:

    @staticmethod
    def create(document_type: DocumentType):

        if document_type == DocumentType.PDF:
            return PDFReader()

        if document_type == DocumentType.WORD:
            return WordReader()

        if document_type == DocumentType.EXCEL:
            return ExcelReader()

        if document_type == DocumentType.POWERPOINT:
            return PPTReader()

        if document_type == DocumentType.TEXT:
            return TxtReader()

        raise ValueError(f"Unsupported document type : {document_type}")