from models.document import DocumentData


class MetadataBuilder:

    def build(self, document: DocumentData) -> DocumentData:

        total = len(document.chunks)

        for chunk in document.chunks:

            metadata = {
                key: value for key, value in document.metadata.items()
                if isinstance(value, (str, int, float, bool)) and value is not None
            }
            metadata.update({
                "file_name": document.file_name,
                "file_type": document.file_type,
                "chunk_id": chunk.chunk_id,
                "total_chunks": total,
                "total_pages": document.total_pages,
            })
            chunk.metadata = metadata

        return document
