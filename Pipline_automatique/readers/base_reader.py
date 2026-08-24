"""
Abstract base class for all document readers.
"""

from abc import ABC, abstractmethod


class BaseReader(ABC):
    """
    Base interface for every document reader.
    """

    @abstractmethod
    def read(self, file_path: str):
        """
        Read a document and return its extracted content.
        """
        pass