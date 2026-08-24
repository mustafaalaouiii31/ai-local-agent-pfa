from typing import Any, Optional
from RAG.retriever import Retriever
from RAG.context_builder import ContextBuilder
from LLM.response_generator import ResponseGenerator


class RAGPipeline:
    """RAG restricted to the documents explicitly selected by the user."""

    def __init__(self, top_k=4, max_context_chunks=4, model_name="llama3.2"):
        self.retriever = Retriever(top_k=top_k)
        self.context_builder = ContextBuilder(max_chunks=max_context_chunks)
        self.response_generator = ResponseGenerator(model_name=model_name)

    def retrieve(self, query: str, document_names: Optional[list[str]] = None) -> list[dict[str, Any]]:
        if not document_names:
            return []
        return self.retriever.retrieve(query, document_names=document_names)

    def build_context(self, query, document_names=None):
        return self.context_builder.build(self.retrieve(query, document_names))

    def generate_answer(self, query, document_names=None):
        if not document_names:
            return {
                "answer": "Aucun document n'est sélectionné.",
                "found": False, "document_names": [], "sources": [],
            }

        chunks = self.retrieve(query, document_names)
        if not chunks:
            return {
                "answer": "Je ne trouve pas cette information dans les documents sélectionnés.",
                "found": False, "document_names": document_names, "sources": [],
            }

        context = self.context_builder.build(chunks)
        answer = self.response_generator.generate(question=query, context=context)

        sources = []
        for chunk in chunks:
            name = chunk.get("metadata", {}).get("file_name")
            if name and name not in sources:
                sources.append(name)

        return {
            "answer": answer,
            "found": True,
            "document_names": document_names,
            "sources": sources,
        }

    def ask(self, query, document_names=None):
        return self.generate_answer(query, document_names)["answer"]
