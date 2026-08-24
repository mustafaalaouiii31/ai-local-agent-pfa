"""
Semantic Chunker using LangChain.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.document import DocumentData
from models.chunk import ChunkData


class Chunker:

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=chunk_size,

            chunk_overlap=chunk_overlap,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def chunk(self, document: DocumentData) -> DocumentData:

        texts = self.splitter.split_text(document.cleaned_text)

        chunks = []

        for index, text in enumerate(texts, start=1):

            chunks.append(

                ChunkData(

                    chunk_id=index,

                    text=text

                )

            )

        document.chunks = chunks

        return document