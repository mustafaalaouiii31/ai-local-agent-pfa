from RAG.rag_pipeline import RAGPipeline
from .intent_detector import IntentDetector
from Agent.workflows.summary_workflow import SummaryWorkflow
from Agent.workflows.comparison_workflow import ComparisonWorkflow
from Agent.workflows.decission_workflow import DecisionWorkflow
from LLM.direct_llm import DirectLLM


class AgentOrchestrator:
    """Routes every request according to active documents and intent."""

    def __init__(self, model_name="llama3.2", top_k=5, max_context_chunks=5):
        self.intent_detector = IntentDetector(model_name=model_name)
        self.direct_llm = DirectLLM(model_name=model_name)
        self.rag = RAGPipeline(
            top_k=top_k,
            max_context_chunks=max_context_chunks,
            model_name=model_name,
        )
        self.summary_workflow = SummaryWorkflow(model_name=model_name)
        self.comparison_workflow = ComparisonWorkflow(model_name=model_name)
        self.decission_workflow = DecisionWorkflow(model_name=model_name)

    @staticmethod
    def _docs(names):
        if not names:
            return []
        return list(dict.fromkeys(
            n.strip() for n in names if isinstance(n, str) and n.strip()
        ))

    def process(self, query, document_names=None, force_ollama=False):
        query = (query or "").strip()
        documents = self._docs(document_names)

        if not query:
            return {
                "query": query, "scope": "general", "intent": "question",
                "answer": "Veuillez entrer une question.", "document_names": [],
                "sources": [], "needs_ollama": False,
            }

        # Explicit approval from the UI: Ollama may now use general knowledge.
        if force_ollama:
            return {
                "query": query, "scope": "general", "intent": "question",
                "answer": self.direct_llm.ask(query),
                "document_names": documents, "sources": [],
                "needs_ollama": False, "used_ollama": True,
            }

        # No active document = normal Ollama mode.
        # CORRECTION : on ne classe même pas l'intention dans ce cas.
        # Le nouvel IntentDetector renvoie de toute façon
        # scope="general" quand aucun document n'est sélectionné (voir
        # sa règle 2), donc l'appeler ici n'aurait aucun effet sur la
        # réponse — juste un aller-retour LLM inutile pour chaque
        # question générale.
        if not documents:
            return {
                "query": query, "scope": "general", "intent": "question",
                "answer": self.direct_llm.ask(query), "document_names": [],
                "sources": [], "needs_ollama": False, "used_ollama": True,
            }

        # CORRECTION : le nouvel IntentDetector.detect() prend maintenant
        # document_names en paramètre pour donner au LLM le contexte réel
        # des documents sélectionnés (au lieu de deviner à l'aveugle si
        # "ce fichier" désigne quelque chose). On lui transmet donc les
        # documents actifs.
        classification = self.intent_detector.detect(query, document_names=documents)
        intent = classification.get("intent", "question") if isinstance(classification, dict) else "question"

        # Documents are active: NEVER answer from general knowledge first.
        if intent == "summary":
            result = self.summary_workflow.run(query, document_names=documents)
        elif intent == "comparison":
            result = self.comparison_workflow.run(query, document_names=documents)
        elif intent == "recommendation":
            result = self.decission_workflow.run(query, document_names=documents)
        else:
            result = self.rag.generate_answer(query, document_names=documents)

        if not result.get("found", False):
            return {
                "query": query,
                "scope": "document",
                "intent": intent,
                "answer": (
                    "Je ne trouve pas cette information dans les documents sélectionnés.\n\n"
                    "Voulez-vous utiliser Ollama pour répondre avec ses connaissances générales ?"
                ),
                "document_names": documents,
                "sources": [],
                "needs_ollama": True,
                "used_ollama": False,
            }

        return {
            "query": query,
            "scope": "document",
            "intent": intent,
            "answer": result.get("answer", ""),
            "document_names": result.get("document_names", documents),
            "sources": result.get("sources", documents),
            "needs_ollama": False,
            "used_ollama": False,
        }