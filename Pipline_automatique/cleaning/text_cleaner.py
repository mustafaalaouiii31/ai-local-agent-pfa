"""
Text Cleaner

Clean extracted text before chunking.
"""

import re

from models.document import DocumentData


class TextCleaner:
    """
    Clean the extracted text from a document.
    """

    def __init__(
        self,
        remove_extra_spaces: bool = True,
        remove_empty_lines: bool = True,
        normalize_newlines: bool = True,
        remove_control_characters: bool = True,
    ):
        self.remove_extra_spaces = remove_extra_spaces
        self.remove_empty_lines = remove_empty_lines
        self.normalize_newlines = normalize_newlines
        self.remove_control_characters = remove_control_characters

    def clean(self, document: DocumentData) -> DocumentData:
        """
        Clean document.raw_text and store the result in
        document.cleaned_text.
        """

        text = document.raw_text

        # Remove control characters
        if self.remove_control_characters:
            text = self._remove_control_characters(text)

        # Remove extra spaces
        if self.remove_extra_spaces:
            text = self._remove_extra_spaces(text)

        # Remove empty lines
        if self.remove_empty_lines:
            text = self._remove_empty_lines(text)

        # Normalize newlines
        if self.normalize_newlines:
            text = self._normalize_newlines(text)

        document.cleaned_text = text

        return document

    def _remove_extra_spaces(self, text: str) -> str:
        """
        Replace multiple spaces with one.
        """
        return re.sub(r"[ \t]+", " ", text)

    def _remove_empty_lines(self, text: str) -> str:
        """
        Remove empty lines.
        """
        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:
                lines.append(line)

        return "\n".join(lines)

    def _normalize_newlines(self, text: str) -> str:
        """
        Replace multiple newlines with two.
        """
        return re.sub(r"\n{3,}", "\n\n", text)

    def _remove_control_characters(self, text: str) -> str:
        """
        Remove invisible characters.
        """
        return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)