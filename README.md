# AI Local Agent

Assistant IA local d'aide à la décision, construit avec **Streamlit**. L'application communique avec un `AgentOrchestrator` qui route chaque requête entre :

- un pipeline **RAG** (recherche + génération) appuyé sur **ChromaDB** pour la mémoire documentaire,
- des workflows dédiés pour le **résumé**, la **comparaison** et l'**aide à la décision**,
- **Ollama** (modèle local `llama3.2`) pour les questions générales ou en relais explicite quand l'information n'est pas dans les documents sélectionnés.

## Fonctionnalités

- Upload et indexation de documents (PDF, DOCX, XLSX, PPTX, TXT) dans une mémoire vectorielle locale (ChromaDB).
- Sélection manuelle des documents à utiliser pour chaque question (« Documents utilisés »).
- Détection d'intention (résumé / comparaison / recommandation / question) via LLM, avec le contexte des documents actifs.
- Relais explicite vers Ollama (connaissances générales) quand l'information demandée n'est pas dans les documents, avec confirmation de l'utilisateur.
- Historique de conversations persistant (sauvegardé sur disque, plusieurs discussions, suppression possible).
- 100% local : aucune donnée n'est envoyée à un service externe.

## Prérequis

- Python 3.10+
- [Ollama](https://ollama.com) installé, avec le modèle `llama3.2` téléchargé :
  ```bash
  ollama pull llama3.2
  ```

## Installation

```bash
pip install -r requirements.txt
```

## Lancer l'application

```bash
streamlit run app.py
```

Ouvrez ensuite l'URL locale affichée dans le terminal (par défaut `http://localhost:8501`).

## Structure du projet

```
app.py                     # Interface Streamlit (point d'entrée)
Agent/                     # Orchestrateur, détection d'intention, workflows (résumé/comparaison/décision)
RAG/                       # Pipeline RAG (retriever, contexte, génération de réponse)
LLM/                       # Clients LLM (Ollama, génération de réponses)
Pipline_automatique/       # Ingestion des documents (lecture, nettoyage, chunking, embeddings, indexation)
Memory/                    # Mémoire court/long terme et procédurale
Web/                       # Service de recherche web
ui/                        # Styles de l'interface
models/                    # Modèles de données (Document, Chunk)
```

## Notes

- `data/uploads/`, `data/chat_history.json` et `database/` (ChromaDB) sont générés localement et ne sont pas versionnés (voir `.gitignore`) — ils contiennent respectivement vos documents importés, votre historique de conversations, et l'index vectoriel.
- Le modèle Ollama (`llama3.2` par défaut) doit être lancé localement (`ollama serve`, généralement démarré automatiquement) pour que l'application fonctionne.
