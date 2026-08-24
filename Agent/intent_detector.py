"""
Intent Detector

Uses the local Ollama LLM to understand what the user actually wants.
It detects:
- scope: general / document
- intent: question / summary / comparison / recommendation
"""

import json
import re

from LLM.ollama_client import OllamaClient


class IntentDetector:
    """
    Understands the user's request using Ollama.
    """

    def __init__(
        self,
        model_name: str = "llama3.2"
    ):
        self.client = OllamaClient(
            model_name=model_name
        )

    def detect(
        self,
        query: str,
        document_names: list[str] | None = None
    ) -> dict:

        documents = document_names or []

        documents_text = (
            "\n".join(
                f"- {name}"
                for name in documents
            )
            if documents
            else "Aucun document sélectionné."
        )

        prompt = f"""
Tu es le module de compréhension d'un agent IA local.

Ta tâche est UNIQUEMENT de comprendre la demande
de l'utilisateur et de déterminer comment l'agent
doit la traiter.

==================================================
DOCUMENTS ACTUELLEMENT SÉLECTIONNÉS
==================================================

{documents_text}

==================================================
QUESTION UTILISATEUR
==================================================

{query}

==================================================
RÈGLES
==================================================

1. Si l'utilisateur parle d'un fichier, d'un document,
   de données, d'un tableau ou demande de travailler
   sur un document sélectionné :

   scope = "document"

2. Si aucun document n'est sélectionné et que la question
   est une question générale :

   scope = "general"

3. "résume", "resume", "fais un résumé", "résume ce fichier",
   "résume ce document", "donne-moi un résumé", etc.

   intent = "summary"

4. "compare", "comparer", "quelle est la différence",
   "compare ces fichiers", etc.

   intent = "comparison"

5. "quel est le meilleur", "que choisir", "recommande-moi",
   "quelle solution choisir", "aide-moi à décider", etc.

   intent = "recommendation"

6. Une demande d'information classique :

   intent = "question"

==================================================
IMPORTANT
==================================================

Ne te limite PAS aux mots exacts.

Tu dois comprendre le sens de la demande.

Exemples :

Question :
"resume ce fichier"

Documents :
["donnees_cybersecurite.xlsx"]

Résultat :
{{
    "scope": "document",
    "intent": "summary"
}}

---

Question :
"qu'est-ce qu'il contient ?"

Documents :
["test.xlsx"]

Résultat :
{{
    "scope": "document",
    "intent": "question"
}}

---

Question :
"donne-moi les composants de ce fichier"

Documents :
["test.xlsx"]

Résultat :
{{
    "scope": "document",
    "intent": "question"
}}

---

Question :
"compare les deux CV"

Documents :
["CV1.pdf", "CV2.pdf"]

Résultat :
{{
    "scope": "document",
    "intent": "comparison"
}}

---

Question :
"quel candidat choisir ?"

Documents :
["CV1.pdf", "CV2.pdf"]

Résultat :
{{
    "scope": "document",
    "intent": "recommendation"
}}

---

Question :
"explique la deuxième loi de Newton"

Documents :
Aucun document sélectionné.

Résultat :
{{
    "scope": "general",
    "intent": "question"
}}

==================================================
RÉPONSE
==================================================

Retourne UNIQUEMENT un JSON valide.

Format obligatoire :

{{
    "scope": "general" ou "document",
    "intent": "question" ou "summary" ou "comparison" ou "recommendation"
}}
"""

        try:

            response = self.client.generate(
                prompt
            )

            return self._parse_response(
                response
            )

        except Exception as e:

            print(
                f"[IntentDetector] Erreur Ollama : {e}"
            )

            # Fallback sécurisé
            if documents:
                return {
                    "scope": "document",
                    "intent": "question"
                }

            return {
                "scope": "general",
                "intent": "question"
            }

    def _parse_response(
        self,
        response: str
    ) -> dict:

        if not response:
            return {
                "scope": "general",
                "intent": "question"
            }

        response = response.strip()

        # Retirer éventuellement ```json ... ```
        response = re.sub(
            r"```json\s*",
            "",
            response,
            flags=re.IGNORECASE
        )

        response = re.sub(
            r"```\s*$",
            "",
            response
        )

        # Chercher le JSON
        match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
        )

        if not match:
            return {
                "scope": "general",
                "intent": "question"
            }

        try:

            data = json.loads(
                match.group(0)
            )

        except json.JSONDecodeError:

            return {
                "scope": "general",
                "intent": "question"
            }

        scope = data.get(
            "scope",
            "general"
        )

        intent = data.get(
            "intent",
            "question"
        )

        if scope not in {
            "general",
            "document"
        }:
            scope = "general"

        if intent not in {
            "question",
            "summary",
            "comparison",
            "recommendation"
        }:
            intent = "question"

        return {
            "scope": scope,
            "intent": intent
        }