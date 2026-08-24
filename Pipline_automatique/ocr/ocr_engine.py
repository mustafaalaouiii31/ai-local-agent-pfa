"""
OCR Engine using EasyOCR.
"""

from typing import List

import easyocr
from PIL import Image


class OCREngine:
    """
    OCR engine based on EasyOCR.
    """

    def __init__(self, languages=None):

        if languages is None:
            languages = ["en", "fr"]

        self.reader = easyocr.Reader(languages)

    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from a single image.
        """

        results = self.reader.readtext(image)

        text = []

        for result in results:

            text.append(result[1])

        return "\n".join(text)

    def extract_pages(self, images: List[Image.Image]) -> str:
        """
        OCR all pages.
        """

        pages = []

        for image in images:

            pages.append(self.extract_text(image))

        return "\n\n".join(pages)