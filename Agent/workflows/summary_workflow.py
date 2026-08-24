"""
Summary Workflow

Generates summaries from documents stored
in the local ChromaDB database.

The workflow supports:

- one selected document;
- multiple selected documents;
- explicit document names;
- references such as:
    "ce document"
    "ce fichier"
    "cette présentation".

Hierarchical summarization is used:

1. Retrieve document chunks.
2. Split chunks into groups.
3. Generate intermediate summaries.
4. Generate final summary.
"""

from LLM.response_generator import ResponseGenerator
from Pipline_automatique.indexing.chroma_indexer import ChromaIndexer


class SummaryWorkflow:
    """
    Workflow responsible for document summarization.
    """

    def __init__(
        self,
        model_name: str = "llama3.2",
        chunks_per_group: int = 5,
    ):

        # ==================================================
        # CHROMADB
        # ==================================================

        self.indexer = ChromaIndexer()

        # ==================================================
        # LLM
        # ==================================================

        self.response_generator = ResponseGenerator(
            model_name=model_name
        )

        self.chunks_per_group = chunks_per_group

    # ==================================================
    # RUN
    # ==================================================

    def run(
        self,
        query: str,
        document_names: list[str] | None = None
    ) -> dict:
        """
        Generate a summary.

        Parameters
        ----------
        query : str
            User request.

        document_names : list[str] | None
            Documents selected in the interface.

        Returns
        -------
        dict
            {
                "answer": str,
                "document_names": list[str],
                "found": bool,
            }
        """

        # ==================================================
        # NORMALIZE DOCUMENT NAMES
        # ==================================================

        document_names = self._normalize_document_names(
            document_names
        )

        # ==================================================
        # FIND DOCUMENTS
        # ==================================================

        selected_documents = self._resolve_documents(
            query=query,
            document_names=document_names
        )

        # ==================================================
        # NO DOCUMENT
        # ==================================================

        if not selected_documents:

            # CORRECTION : "found" manquait ici. orchestrator.py fait
            # `if not result.get("found", False):` — sans cette clé,
            # la valeur par défaut (False) déclenchait TOUJOURS le
            # message générique "je ne trouve pas" + la question
            # Ollama, y compris quand ce n'était pas voulu ici (on
            # demande juste de choisir un document, ce n'est pas un
            # échec de recherche).
            return {
                "answer": (
                    "Quel document souhaitez-vous résumer ?\n\n"
                    "Veuillez sélectionner un document "
                    "dans la mémoire documentaire."
                ),
                "document_names": [],
                "found": False,
            }

        print(
            f"[Summary] Documents utilisés : "
            f"{selected_documents}"
        )

        # ==================================================
        # RETRIEVE ALL CHUNKS
        # ==================================================

        all_chunks = []

        for document_name in selected_documents:

            chunks = self.indexer.get_document_chunks(
                document_name
            )

            if not chunks:
                print(
                    f"[Summary] Aucun chunk trouvé pour : "
                    f"{document_name}"
                )
                continue

            # Add document information explicitly
            for chunk in chunks:

                metadata = chunk.get(
                    "metadata",
                    {}
                )

                metadata["file_name"] = document_name

                chunk["metadata"] = metadata

                all_chunks.append(chunk)

        # ==================================================
        # NO CONTENT
        # ==================================================

        if not all_chunks:

            # CORRECTION : "found" manquait ici aussi — le document
            # est trouvé mais vide de contenu exploitable, donc c'est
            # un vrai échec (found=False est correct ici, il fallait
            # juste le déclarer explicitement).
            return {
                "answer": (
                    "Je trouve le document dans la mémoire, "
                    "mais aucun contenu exploitable n'a été trouvé."
                ),
                "document_names": selected_documents,
                "found": False,
            }

        print(
            f"[Summary] Nombre total de chunks : "
            f"{len(all_chunks)}"
        )

        # ==================================================
        # CREATE GROUPS
        # ==================================================

        groups = self._create_groups(
            all_chunks
        )

        print(
            f"[Summary] Nombre de groupes : "
            f"{len(groups)}"
        )

        # ==================================================
        # INTERMEDIATE SUMMARIES
        # ==================================================

        intermediate_summaries = []

        for index, group in enumerate(
            groups,
            start=1
        ):

            print(
                f"[Summary] Résumé groupe "
                f"{index}/{len(groups)}"
            )

            context = self._build_context(
                group
            )

            question = self._build_group_question(
                query=query,
                group_index=index,
                total_groups=len(groups)
            )

            summary = self.response_generator.generate(
                question,
                context
            )

            intermediate_summaries.append(
                summary
            )

        # ==================================================
        # FINAL SUMMARY CONTEXT
        # ==================================================

        final_context = self._build_summary_context(
            intermediate_summaries
        )

        # ==================================================
        # FINAL SUMMARY
        # ==================================================

        final_question = self._build_final_question(
            query=query,
            document_names=selected_documents
        )

        final_response = self.response_generator.generate(
            final_question,
            final_context
        )

        # ==================================================
        # RETURN
        # ==================================================

        # CORRECTION : c'est ici le vrai cœur du bug. Ce retour ne
        # contenait AUCUNE clé "found", alors que c'est le cas de
        # succès normal (résumé généré avec du vrai contenu). Sans
        # "found": True explicite, orchestrator.py jetait ce résumé
        # pourtant valide et affichait "je ne trouve pas cette
        # information" à la place, à chaque fois.
        return {
            "answer": final_response,
            "document_names": selected_documents,
            "found": True,
        }

    # ==================================================
    # NORMALIZE DOCUMENT NAMES
    # ==================================================

    def _normalize_document_names(
        self,
        document_names: list[str] | None
    ) -> list[str]:

        if not document_names:
            return []

        normalized = []

        for name in document_names:

            if not name:
                continue

            name = str(name).strip()

            if not name:
                continue

            if name not in normalized:

                normalized.append(name)

        return normalized

    # ==================================================
    # RESOLVE DOCUMENTS
    # ==================================================

    def _resolve_documents(
        self,
        query: str,
        document_names: list[str]
    ) -> list[str]:
        """
        Determine which documents should be summarized.

        Priority:

        1. Explicitly selected documents.
        2. Document explicitly mentioned in the query.
        3. If only one document exists, use it.
        4. Otherwise ask the user to select a document.
        """

        # --------------------------------------------------
        # 1. USER SELECTED DOCUMENTS
        # --------------------------------------------------

        if document_names:

            return document_names

        # --------------------------------------------------
        # 2. SEARCH DOCUMENT NAME IN QUERY
        # --------------------------------------------------

        available_documents = (
            self._get_available_document_names()
        )

        query_lower = query.lower()

        explicit_matches = []

        for document_name in available_documents:

            if document_name.lower() in query_lower:

                explicit_matches.append(
                    document_name
                )

        if explicit_matches:

            return explicit_matches

        # --------------------------------------------------
        # 3. ONLY ONE DOCUMENT AVAILABLE
        # --------------------------------------------------

        if len(available_documents) == 1:

            return [
                available_documents[0]
            ]

        # --------------------------------------------------
        # 4. MULTIPLE DOCUMENTS
        # --------------------------------------------------

        return []

    # ==================================================
    # GET AVAILABLE DOCUMENTS
    # ==================================================

    def _get_available_document_names(
        self
    ) -> list[str]:
        """
        Return unique document names stored in ChromaDB.
        """

        results = self.indexer.collection.get()

        metadatas = results.get(
            "metadatas",
            []
        )

        document_names = []

        for metadata in metadatas:

            if not metadata:
                continue

            file_name = metadata.get(
                "file_name"
            )

            if not file_name:
                continue

            if file_name not in document_names:

                document_names.append(
                    file_name
                )

        return document_names

    # ==================================================
    # CREATE GROUPS
    # ==================================================

    def _create_groups(
        self,
        chunks: list[dict]
    ) -> list[list[dict]]:
        """
        Divide chunks into groups.
        """

        groups = []

        for i in range(
            0,
            len(chunks),
            self.chunks_per_group
        ):

            groups.append(
                chunks[
                    i:i + self.chunks_per_group
                ]
            )

        return groups

    # ==================================================
    # BUILD CHUNK CONTEXT
    # ==================================================

    def _build_context(
        self,
        chunks: list[dict]
    ) -> str:
        """
        Build context from document chunks.
        """

        context_parts = []

        for index, chunk in enumerate(
            chunks,
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

        return "\n".join(
            context_parts
        )

    # ==================================================
    # GROUP QUESTION
    # ==================================================

    def _build_group_question(
        self,
        query: str,
        group_index: int,
        total_groups: int
    ) -> str:
        """
        Build prompt for intermediate summary.
        """

        return f"""
Tu es le module de résumé d'un agent IA local.

L'utilisateur demande :

{query}

Tu dois résumer uniquement la partie du document
présente dans le contexte.

Il s'agit du groupe {group_index}
sur {total_groups}.

RÈGLES :

- Utilise uniquement le contexte fourni.
- N'invente aucune information.
- Conserve les informations importantes.
- Supprime les détails inutiles.
- Reste fidèle au document.
- Ne complète pas le document avec tes connaissances.
- Réponds en français.
- Si plusieurs documents apparaissent dans le contexte,
  conserve leur séparation.

Produis uniquement le résumé de cette partie.
"""

    # ==================================================
    # BUILD SUMMARY CONTEXT
    # ==================================================

    def _build_summary_context(
        self,
        summaries: list[str]
    ) -> str:
        """
        Build context for final summary.
        """

        context_parts = []

        for index, summary in enumerate(
            summaries,
            start=1
        ):

            context_parts.append(
                f"""
RÉSUMÉ INTERMÉDIAIRE {index}

{summary}
"""
            )

        return "\n".join(
            context_parts
        )

    # ==================================================
    # FINAL QUESTION
    # ==================================================

    def _build_final_question(
        self,
        query: str,
        document_names: list[str]
    ) -> str:
        """
        Build final summary prompt.
        """

        documents = "\n".join(
            f"- {name}"
            for name in document_names
        )

        return f"""
Tu es le module de résumé final d'un agent IA local.

L'utilisateur demande :

{query}

DOCUMENT(S) RÉSUMÉ(S) :

{documents}

Tu disposes maintenant de plusieurs résumés
intermédiaires provenant du ou des documents demandés.

Produis un résumé final clair et cohérent.

RÈGLES :

- Utilise uniquement les résumés intermédiaires.
- N'invente aucune information.
- Ne complète pas avec tes connaissances générales.
- Supprime les répétitions.
- Conserve les informations importantes.
- Réponds en français.
- Si plusieurs documents sont résumés, indique clairement
  les informations provenant de chaque document lorsque
  cela est nécessaire.
- Ne prétends pas avoir utilisé des sources externes.

STRUCTURE CONSEILLÉE :

1. Résumé général
2. Points importants
3. Informations principales

Si plusieurs documents sont concernés :

DOCUMENT 1
...

DOCUMENT 2
...

Produis directement le résumé final.
"""