"""
Prompt Builder

Builds the prompt sent to the local LLM
using only the context retrieved by the RAG.
"""


class PromptBuilder:
    """
    Build controlled prompts for the local LLM.
    """

    def build(
        self,
        question: str,
        context: str
    ) -> str:
        """
        Build a prompt using the user question
        and retrieved document context.
        """

        prompt = f"""
Tu es un assistant IA local d'aide à la décision.

Ta mission est de répondre à la question de l'utilisateur
UNIQUEMENT à partir du CONTEXTE fourni.

RÈGLES IMPORTANTES :

1. Utilise uniquement les informations présentes dans le contexte.
2. N'utilise pas tes connaissances générales.
3. N'invente aucune information.
4. Si la réponse n'est pas présente dans le contexte,
   réponds clairement :
   "Information non disponible dans les documents."
5. Donne une réponse claire, structurée et concise.
6. Lorsque c'est possible, indique la source utilisée.

========================
CONTEXTE
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

        return prompt
