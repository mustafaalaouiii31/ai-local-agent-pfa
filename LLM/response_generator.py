"""
Response Generator

Generates responses using either:
1. Document context from the local RAG system.
2. General knowledge from the local LLM.
"""

from LLM.llm_client import LLMClient


class ResponseGenerator:
    """
    Generate responses for the local AI agent.
    """

    def __init__(
        self,
        model_name: str = "llama3.2"
    ):
        self.llm_client = LLMClient(
            model_name=model_name
        )

    # ==================================================
    # DOCUMENT MODE
    # ==================================================

    def generate(
        self,
        question: str,
        context: str
    ) -> str:
        """
        Generate an answer using ONLY
        the provided document context.
        """

        prompt = f"""
Tu es un assistant IA local.

Tu dois répondre à la question de l'utilisateur
UNIQUEMENT à partir du CONTEXTE DOCUMENTAIRE fourni.

RÈGLES :

- Utilise uniquement les informations du contexte.
- N'utilise aucune connaissance extérieure.
- N'invente aucune information.
- Ne complète pas les informations manquantes.
- Si la réponse n'est pas présente dans le contexte,
  réponds exactement :

"Information non disponible dans les documents."

- Sois clair et précis.
- Si une source est disponible dans le contexte,
  indique le document utilisé.

========================
CONTEXTE DOCUMENTAIRE
========================

{context}

========================
QUESTION
========================

{question}

========================
RÉPONSE
========================
"""

        return self.llm_client.generate(prompt)

    # ==================================================
    # GENERAL MODE
    # ==================================================

    def generate_general(
        self,
        question: str
    ) -> str:
        """
        Generate an answer using the general knowledge
        of the local LLM.

        This mode is NOT restricted to documents.
        """

        prompt = f"""
Tu es un assistant IA local.

Réponds directement à la question de l'utilisateur.

Tu peux utiliser tes connaissances générales
pour répondre.

RÈGLES :

- Réponds directement à la question.
- Sois clair, précis et pédagogique.
- N'invente pas de faits.
- Si tu n'es pas certain d'une information,
  indique clairement ton incertitude.
- Ne parle pas de documents si la question
  ne concerne pas les documents.
- Ne réponds pas "Information non disponible
  dans les documents" simplement parce qu'aucun
  document n'est fourni.

QUESTION :

{question}

RÉPONSE :
"""

        return self.llm_client.generate(prompt)