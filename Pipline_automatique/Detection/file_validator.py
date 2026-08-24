"""
Validate uploaded files before processing.
"""

from pathlib import Path


class FileValidator:
    """
    Validate existence, extension and size of a document.
    """

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".xlsx",
        ".pptx",
        ".txt",
    }

    MAX_FILE_SIZE_MB = 100

    @classmethod
    def exists(cls, file_path: str) -> bool:
        return Path(file_path).exists()

    @classmethod
    def validate_extension(cls, file_path: str) -> bool:
        extension = Path(file_path).suffix.lower()
        return extension in cls.ALLOWED_EXTENSIONS

    @classmethod
    def validate_size(cls, file_path: str) -> bool:
        size_mb = Path(file_path).stat().st_size / (1024 * 1024)
        return size_mb <= cls.MAX_FILE_SIZE_MB

    @classmethod
    def validate(cls, file_path: str):

        if not cls.exists(file_path):
            raise FileNotFoundError(f"File not found : {file_path}")

        if not cls.validate_extension(file_path):
            raise ValueError(
                f"Unsupported extension : {Path(file_path).suffix}"
            )

        if not cls.validate_size(file_path):
            raise ValueError(
                f"File exceeds {cls.MAX_FILE_SIZE_MB} MB."
            )

        return True