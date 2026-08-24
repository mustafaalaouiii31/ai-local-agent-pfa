"""
PDF Scanner

Convert each page of a PDF into an image.
"""

from pathlib import Path
from typing import List

import fitz
from PIL import Image


class PDFScanner:
    """
    Convert PDF pages into PIL Images.
    """

    def scan(self, file_path: str, dpi: int = 300) -> List[Image.Image]:
        """
        Convert a PDF into a list of PIL Images.

        Parameters
        ----------
        file_path : str
            Path to the PDF.

        dpi : int
            Image quality.

        Returns
        -------
        List[PIL.Image]
        """

        pdf = fitz.open(file_path)

        images = []

        zoom = dpi / 72

        matrix = fitz.Matrix(zoom, zoom)

        for page in pdf:

            pix = page.get_pixmap(matrix=matrix)

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            images.append(image)

        pdf.close()

        return images