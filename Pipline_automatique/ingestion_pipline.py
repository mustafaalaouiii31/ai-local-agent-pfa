"""
Main ingestion pipeline.

This class orchestrates the complete document ingestion workflow.
"""

from models.document import DocumentData

from Pipline_automatique.Detection.document_detector import DocumentDetector
from Pipline_automatique.Detection.file_validator import FileValidator

from  Pipline_automatique.readers.reader_factory import ReaderFactory

from  Pipline_automatique.ocr.pdf_scanner import PDFScanner
from  Pipline_automatique.ocr.ocr_engine import OCREngine

from  Pipline_automatique.cleaning.text_cleaner import TextCleaner

from  Pipline_automatique.chunking.chunker import Chunker
from  Pipline_automatique.chunking.metadata_builder import MetadataBuilder
from  Pipline_automatique.embeddings.embedding_generator import get_embedding_generator

from  Pipline_automatique.indexing.chroma_indexer import ChromaIndexer


class IngestionPipeline:

    def __init__(self):

        self.validator = FileValidator()

        self.detector = DocumentDetector()

        self.cleaner = TextCleaner()

        self.chunker = Chunker()

        self.metadata_builder = MetadataBuilder()

        self.embedding_generator = get_embedding_generator()

        self.indexer = ChromaIndexer()

        self.pdf_scanner = PDFScanner()

        self.ocr = OCREngine()

    def process(self, file_path: str) -> DocumentData:
        """
        Execute the complete ingestion pipeline.
        """

        # Step 1 : Validate file
        self.validator.validate(file_path)

        # Step 2 : Detect document type
        document_type = self.detector.detect(file_path)

        # Step 3 : Read document
        reader = ReaderFactory.create(document_type)

        document = reader.read(file_path)

        # Step 4 : OCR if needed
        if (
            document.file_type == "pdf"
            and len(document.raw_text.strip()) < 50
        ):

            images = self.pdf_scanner.scan(file_path)

            document.raw_text = self.ocr.extract_pages(images)

        # Step 5 : Clean text
        document = self.cleaner.clean(document)

        # Step 6 : Chunk
        document = self.chunker.chunk(document)

        # Step 7 : Metadata
        document = self.metadata_builder.build(document)

        # Step 8 : Embeddings
        document = self.embedding_generator.generate(document)

        # Step 9 : Store in ChromaDB
        self.indexer.store(document)

        return document
