"""
PDF Reader

Reads PDF documents and returns a DocumentData object.
"""

from pathlib import Path
import fitz  # PyMuPDF

from models.document import DocumentData
from Pipline_automatique.Detection.document_detector import DocumentType
from .base_reader import BaseReader


class PDFReader(BaseReader):
    """
    Reader responsible for extracting text and metadata from PDF files.
    """

    def read(self, file_path: str) -> DocumentData:
        """
        Read a PDF file.

        Parameters
        ----------
        file_path : str
            Path to the PDF document.

        Returns
        -------
        DocumentData
            Document filled with extracted information.
        """

        pdf = fitz.open(file_path)

        raw_text = ""

        # Read every page
        for page in pdf:
            raw_text += page.get_text()

        # PDF Metadata
        pdf_metadata = pdf.metadata

        # Build DocumentData
        document = DocumentData(

         file_name=Path(file_path).name,
         file_path=file_path,
         file_type=DocumentType.PDF.value,
         raw_text=raw_text,
         total_pages=len(pdf),
         metadata={
          "title": pdf_metadata.get("title"),
          "author": pdf_metadata.get("author"),
          "subject": pdf_metadata.get("subject"),
          "keywords": pdf_metadata.get("keywords"),
          "creator": pdf_metadata.get("creator"),
          "producer": pdf_metadata.get("producer"),
          "creationDate": pdf_metadata.get("creationDate"),
          "modDate": pdf_metadata.get("modDate"),
        },
        )

        pdf.close()

        return document