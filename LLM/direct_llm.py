"""
Direct LLM

Used for general questions that do not require
document retrieval.
"""

from LLM.ollama_client import OllamaClient


class DirectLLM:
    """
    Handles general questions directly with Ollama.
    """

    def __init__(
        self,
        model_name: str = "llama3.2"
    ):

        self.client = OllamaClient(
            model_name=model_name
        )

    def ask(
        self,
        query: str
    ) -> str:

        if not query or not query.strip():

            return (
                "Veuillez entrer une question."
            )

        prompt = f"""
Tu es un assistant IA local.

Réponds directement à la question de l'utilisateur.

Règles :

- Réponds en français.
- Sois clair et naturel.
- Explique suffisamment pour être utile.
- N'invente pas de faits.
- N'affirme pas avoir consulté des documents.
- Cette question ne nécessite pas de mémoire documentaire.
- Ne parle pas de RAG.
- Ne parle pas de ChromaDB.
- Ne parle pas de l'architecture interne de l'agent.

Question :

{query}

Réponse :
"""

        try:

            return self.client.generate(
                prompt
            )

        except Exception as e:

            return (
                f"Une erreur est survenue lors "
                f"de la génération de la réponse : {e}"
            )