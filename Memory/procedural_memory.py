"""
Procedural Memory

Stores permanent rules, instructions and strategies
used by the AI agent.
"""


class ProceduralMemory:

    def __init__(self):

        self.rules = [

            (
                "L'agent doit utiliser uniquement "
                "les informations présentes dans les "
                "documents lorsqu'une question documentaire "
                "est posée."
            ),

            (
                "L'agent ne doit jamais inventer "
                "une information absente des documents."
            ),

            (
                "Le contexte de conversation doit être "
                "utilisé pour comprendre les références "
                "comme 'ce document', 'l'autre', 'les deux', "
                "'celui-ci', etc."
            ),

            (
                "Une comparaison doit être basée "
                "sur les informations réellement présentes "
                "dans les documents."
            ),

            (
                "Une recommandation doit être justifiée "
                "par les informations disponibles."
            ),

            (
                "Les documents importés constituent "
                "la source principale pour les questions "
                "documentaires."
            ),

            (
                "L'agent doit signaler lorsqu'une information "
                "n'est pas disponible."
            ),
        ]

        self.tools = [
            "RAG",
            "Résumé",
            "Comparaison",
            "Décision",
            "Mémoire",
        ]

    # ==================================================
    # RULES
    # ==================================================

    def get_rules(self) -> list[str]:

        return list(self.rules)

    # ==================================================
    # TOOLS
    # ==================================================

    def get_tools(self) -> list[str]:

        return list(self.tools)

    # ==================================================
    # CONTEXT
    # ==================================================

    def get_context(self) -> str:

        parts = []

        parts.append(
            "RÈGLES DE L'AGENT:"
        )

        for rule in self.rules:

            parts.append(
                f"- {rule}"
            )

        parts.append(
            "\nOUTILS DISPONIBLES:"
        )

        for tool in self.tools:

            parts.append(
                f"- {tool}"
            )

        return "\n".join(parts)