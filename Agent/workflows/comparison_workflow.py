"""
Comparison Workflow

Compare uniquement les documents sélectionnés.
"""

from typing import Optional

from RAG.retriever import Retriever
from LLM.response_generator import ResponseGenerator


class ComparisonWorkflow:

    def __init__(
        self,
        model_name: str = "llama3.2",
        top_k: int = 5
    ):

        self.retriever = Retriever(
            top_k=top_k
        )

        self.response_generator = ResponseGenerator(
            model_name=model_name
        )

        self.top_k = top_k

    def run(
        self,
        query: str,
        document_names: Optional[list[str]] = None
    ) -> dict:
        # CORRECTION : même problème que decision_workflow.py — ce
        # workflow renvoyait une simple chaîne de caractères (-> str),
        # alors que orchestrator.py appelle `result.get("found", False)`
        # sur la valeur reçue. Sur une string, ça plante avec
        # AttributeError. Tous les retours renvoient maintenant un dict
        # {"answer", "document_names", "found", "sources"}.

        if not document_names:

            return {
                "answer": (
                    "Aucun document n'est disponible "
                    "pour effectuer la comparaison."
                ),
                "document_names": [],
                "found": False,
                "sources": [],
            }

        retrieved_chunks = []

        seen_ids = set()

        # Chaque document est interrogé séparément
        for document_name in document_names:

            chunks = self.retriever.retrieve(
                query,
                document_names=[document_name]
            )

            for chunk in chunks:

                chunk_id = chunk.get(
                    "id",
                    f"{document_name}_{len(retrieved_chunks)}"
                )

                if chunk_id not in seen_ids:

                    retrieved_chunks.append(chunk)

                    seen_ids.add(chunk_id)

        if not retrieved_chunks:

            return {
                "answer": (
                    "Les documents sélectionnés ne contiennent "
                    "pas suffisamment d'informations pour "
                    "effectuer cette comparaison."
                ),
                "document_names": document_names,
                "found": False,
                "sources": [],
            }

        # ======================================================
        # CONTEXTE
        # ======================================================

        context_parts = []

        for index, chunk in enumerate(
            retrieved_chunks,
            start=1
        ):

            text = chunk.get(
                "text",
                ""
            )

            metadata = chunk.get(
                "metadata",
                {}
            )

            file_name = metadata.get(
                "file_name",
                "Document inconnu"
            )

            chunk_id = metadata.get(
                "chunk_id",
                "?"
            )

            context_parts.append(
                f"""
SOURCE {index}

Document : {file_name}
Chunk : {chunk_id}

{text}
"""
            )

        context = "\n".join(
            context_parts
        )

        # ======================================================
        # PROMPT
        # ======================================================

        prompt = f"""
Tu es un assistant IA local.

Tu dois comparer UNIQUEMENT les documents
sélectionnés par l'utilisateur.

DOCUMENTS SÉLECTIONNÉS :
{', '.join(document_names)}

RÈGLE ABSOLUE :

Utilise uniquement les informations présentes
dans le contexte.

N'utilise aucune connaissance générale.

N'invente aucune information.

N'invente aucun avantage.

N'invente aucun inconvénient.

N'invente aucun risque.

N'invente aucun coût.

N'invente aucune performance.

N'invente aucune caractéristique absente.

Si une information n'est pas présente :

"Information non disponible dans les documents."

Pour les CV :

- chaque CV représente un candidat ;
- compare uniquement les informations réellement
  présentes dans les CV ;
- formation ;
- expériences ;
- compétences ;
- technologies ;
- projets ;
- certifications ;
- langues.

Présente une comparaison claire.

À la fin, indique les sources utilisées.

==================================================
CONTEXTE DOCUMENTAIRE
==================================================

{context}

==================================================
QUESTION
==================================================

{query}

==================================================
RÉPONSE
==================================================
"""

        answer = self.response_generator.generate(
            question=prompt,
            context=context
        )

        sources = []

        for chunk in retrieved_chunks:

            name = chunk.get("metadata", {}).get("file_name")

            if name and name not in sources:

                sources.append(name)

        return {
            "answer": answer,
            "document_names": document_names,
            "found": True,
            "sources": sources,
        }