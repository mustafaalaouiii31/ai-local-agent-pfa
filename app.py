import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import streamlit as st

from Agent.orchestrator import AgentOrchestrator
from Pipline_automatique.ingestion_pipline import IngestionPipeline
from Pipline_automatique.indexing.chroma_indexer import ChromaIndexer

st.set_page_config(page_title="ZTE AI Local Agent", page_icon="🤖", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# CORRECTION — Historique persistant : les discussions étaient stockées
# uniquement dans st.session_state.chats, donc perdues à chaque
# redémarrage du serveur Streamlit. Elles sont maintenant sauvegardées
# dans un fichier JSON sur disque et rechargées automatiquement au
# démarrage de l'application.
HISTORY_FILE = BASE_DIR / "data" / "chat_history.json"

st.markdown("""
<style>
:root{--blue:#1687ff;--blue2:#39a7ff;--bg:#06101d;--panel:#0b1726;--line:#183653;--text:#f4f8ff;--muted:#8da6bf;--green:#32d39a;--neon1:#ff3d9a;--neon2:#8b3dff;--neon3:#39a7ff}
.stApp{background:radial-gradient(circle at 70% 0%,rgba(22,135,255,.13),transparent 35%),var(--bg);color:var(--text)}
section[data-testid="stSidebar"]{background:#071321;border-right:1px solid var(--line)}
.sidebar-logo{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,var(--neon3),var(--neon2) 55%,var(--neon1));display:flex;align-items:center;justify-content:center;color:white;font-size:24px;font-weight:800;margin-bottom:10px;box-shadow:0 0 18px rgba(139,61,255,.35)}
.sidebar-title{font-size:18px;font-weight:800}.sidebar-subtitle{font-size:12px;color:var(--muted);margin-bottom:24px}
.topbar{border-bottom:1px solid var(--line);padding:15px 0;margin-bottom:34px;display:flex;justify-content:space-between}.topbar-brand{font-weight:800}.topbar-brand span{background:linear-gradient(90deg,var(--neon3),var(--neon2),var(--neon1));-webkit-background-clip:text;background-clip:text;color:transparent}.topbar-right{color:var(--muted);font-size:13px}
.agent-hero{text-align:center;max-width:850px;margin:auto}.agent-badge{width:68px;height:68px;margin:auto;border-radius:20px;background:linear-gradient(135deg,var(--neon3),var(--neon2) 55%,var(--neon1));display:flex;align-items:center;justify-content:center;color:white;font-size:32px;box-shadow:0 15px 40px rgba(139,61,255,.35)}
.agent-hero h1{font-size:34px;margin:14px 0 5px}.agent-hero p{color:var(--muted)}.agent-status{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;color:var(--muted);font-size:13px;margin-top:15px}.status-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);margin-right:6px;box-shadow:0 0 8px rgba(50,211,154,.7);animation:pulse-dot 2s ease-in-out infinite}
@keyframes pulse-dot{0%,100%{box-shadow:0 0 6px rgba(50,211,154,.6)}50%{box-shadow:0 0 14px rgba(50,211,154,1)}}
.info-box{max-width:850px;margin:22px auto;padding:13px 16px;border:1px solid rgba(22,135,255,.25);background:rgba(22,135,255,.09);border-radius:12px;color:#b9d9ff;font-size:13px}
.sidebar-label{color:#7190ac;font-size:10px;font-weight:800;letter-spacing:1.2px;margin:20px 0 8px}.doc-row{display:flex;gap:8px;align-items:center;padding:8px 3px;border-bottom:1px solid rgba(255,255,255,.04);font-size:12px}.doc-icon{color:#70b7ff}.doc-name{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.doc-count{background:rgba(22,135,255,.14);color:#75bbff;padding:2px 6px;border-radius:7px;font-size:10px}.footer{text-align:center;color:#5d7893;font-size:11px;margin:30px}

/* CORRECTION — Style "dégradés vifs / accent néon" pour les bulles de
   conversation, choisi par l'utilisateur. Message utilisateur : fond en
   dégradé néon plein avec lueur (glow). Message assistant : fond sombre
   avec une bordure en dégradé néon et une lueur plus discrète, pour
   garder les deux rôles bien distincts d'un coup d'œil. */
[data-testid="stChatMessage"]{border-radius:18px;margin-bottom:14px;padding:6px 10px;transition:box-shadow .25s ease}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){
    background:linear-gradient(135deg,var(--neon1),var(--neon2) 60%,var(--neon3));
    border:none;
    box-shadow:0 0 24px rgba(139,61,255,.45),0 0 14px rgba(255,61,154,.35);
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"] p{
    color:#ffffff !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]){
    background:
        linear-gradient(var(--panel),var(--panel)) padding-box,
        linear-gradient(135deg,var(--neon3),var(--neon2),var(--neon1)) border-box;
    border:1.5px solid transparent;
    box-shadow:0 0 16px rgba(57,167,255,.2);
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stMarkdownContainer"]{
    color:var(--text);
}
[data-testid="stChatMessage"] [data-testid="stCaptionContainer"]{color:var(--muted) !important}

/* CORRECTION — Barre de saisie en bas de page :
   1) le conteneur fixe de Streamlit (stBottom / stBottomBlockContainer)
      qui englobe la zone de saisie garde par défaut un fond sombre
      propre à Streamlit, distinct de --bg. On le force à --bg pour
      qu'il se fonde dans le reste de la page.
   2) le contour rouge au focus est la couleur d'accent par défaut de
      Streamlit (#FF4B4B), pas une couleur choisie ici. On la remplace
      par du bleu foncé / blanc. */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"]{background:var(--bg) !important}

[data-testid="stChatInput"]{background:var(--panel) !important;border:1px solid var(--line) !important;border-radius:14px !important}
[data-testid="stChatInput"] [data-baseweb="textarea"]{background:var(--panel) !important;border-color:var(--line) !important;box-shadow:none !important}
[data-testid="stChatInput"] [data-baseweb="textarea"]:focus-within{border-color:var(--blue2) !important;box-shadow:0 0 0 2px rgba(57,167,255,.28) !important}
[data-testid="stChatInput"] textarea{background:transparent !important;color:var(--text) !important;caret-color:#ffffff !important}
[data-testid="stChatInput"] textarea:focus,
[data-testid="stChatInput"] textarea:focus-visible{outline:none !important;box-shadow:none !important;border-color:var(--blue2) !important}
[data-testid="stChatInput"] textarea::placeholder{color:var(--muted) !important}
[data-testid="stChatInputSubmitButton"]{color:var(--blue2) !important}

/* CORRECTION — Style du tag "Documents utilisés" dans le multiselect :
   la couleur rouge/rose venait du thème par défaut de Streamlit
   (couleur d'accent standard), pas d'une règle définie ici — elle
   jurait avec le reste du thème bleu/néon et ressemblait à une erreur.
   On l'aligne sur le dégradé néon utilisé ailleurs. */
[data-testid="stMultiSelect"] [data-baseweb="tag"]{
    background:linear-gradient(135deg,var(--neon3),var(--neon2)) !important;
    border:none !important;
    color:#ffffff !important;
}
[data-testid="stMultiSelect"] [data-baseweb="tag"] span{color:#ffffff !important}
[data-testid="stMultiSelect"] [data-baseweb="tag"] svg{fill:#ffffff !important}
[data-testid="stMultiSelect"] [data-baseweb="select"]{
    background:var(--panel) !important;
    border-color:var(--line) !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_agent():
    return AgentOrchestrator(model_name="llama3.2", top_k=5, max_context_chunks=5)

@st.cache_resource(show_spinner=False)
def load_ingestion():
    return IngestionPipeline()

@st.cache_data(ttl=10, show_spinner=False)
def documents():
    try:
        return ChromaIndexer().get_document_summaries()
    except Exception:
        return []


def index_upload(upload):
    indexer = ChromaIndexer()
    if indexer.document_exists(upload.name):
        return True, f"{upload.name} est déjà indexé."
    path = UPLOAD_DIR / upload.name
    path.write_bytes(upload.getbuffer())
    try:
        load_ingestion().process(str(path))
        documents.clear()
        return True, f"{upload.name} est ajouté et indexé."
    except Exception as exc:
        return False, f"{upload.name} : {exc}"


# CORRECTION — Historique persistant : chargement/sauvegarde sur disque.
def load_history():
    if HISTORY_FILE.is_file():
        try:
            data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return []


def save_history():
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(
            json.dumps(st.session_state.chats, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


def new_chat():
    c={"id":str(uuid4()),"title":"Nouvelle discussion","created_at":datetime.now().isoformat(),"updated_at":datetime.now().isoformat(),"messages":[]}
    st.session_state.chats.insert(0,c);st.session_state.active_id=c["id"]


# CORRECTION — Suppression d'une discussion : bascule sur une autre
# discussion existante (la plus récente) si celle supprimée était active,
# ou en crée une nouvelle vide s'il n'en reste aucune. Sauvegarde
# l'historique sur disque après suppression.
def delete_chat(chat_id):
    st.session_state.chats=[c for c in st.session_state.chats if c["id"]!=chat_id]
    if st.session_state.active_id==chat_id:
        if st.session_state.chats:
            st.session_state.active_id=sorted(st.session_state.chats,key=lambda c:c["updated_at"],reverse=True)[0]["id"]
        else:
            new_chat()
    save_history()


# CORRECTION — Titre de discussion plus pro : au lieu de tronquer
# tel quel le premier message ("Bonjour", "résume moi"...), on demande
# au LLM local un titre court et professionnel. Les documents actifs
# sont donnés en indice pour les messages vagues du type "résume moi".
# En cas d'erreur (Ollama indisponible, etc.), on retombe sur l'ancien
# comportement (texte brut tronqué) pour ne jamais bloquer l'envoi.
def generate_conversation_title(question, active_documents=None):
    fallback = (question or "").strip()[:48] or "Nouvelle discussion"
    try:
        docs_hint = ", ".join((active_documents or [])[:3])
        prompt = (
            "Donne un titre court et professionnel (5 mots maximum, en "
            "français, sans guillemets ni point final) pour une discussion "
            f"qui commence par ce message : \"{question}\"."
        )
        if docs_hint:
            prompt += f" Documents concernés : {docs_hint}."
        prompt += " Réponds uniquement avec le titre, rien d'autre."

        title = load_agent().direct_llm.ask(prompt)
        title = (title or "").strip().strip('"').strip("«»").replace("\n", " ").strip()

        return title[:60] if title else fallback
    except Exception:
        return fallback


# CORRECTION — Demande systématique avant d'utiliser Ollama :
# RAG/rag_pipeline.py est resté sur sa version d'origine, où found=True
# dès que des chunks sont récupérés, même hors-sujet. Comme le fichier
# n'est pas modifié ici, on détecte ce cas côté interface à partir du
# texte de la réponse, et on déclenche quand même la question
# "Voulez-vous utiliser Ollama ?".
_NOT_FOUND_PATTERNS = [
    "non disponible dans les documents",
    "information non disponible",
    "je ne trouve pas",
    "ne trouve pas cette information",
    "aucune information",
    "pas d'information disponible",
    "pas d’information disponible",
    "hors du contexte",
    "n'est pas mentionné",
    "n’est pas mentionné",
    "n'est pas présent dans",
    "n’est pas présent dans",
    "aucun élément ne permet",
    "ne figure pas dans",
]


def answer_not_found(text):
    if not text:
        return True
    lowered = text.lower()
    return any(pattern in lowered for pattern in _NOT_FOUND_PATTERNS)


def current_chat():
    for c in st.session_state.chats:
        if c["id"]==st.session_state.active_id:return c
    new_chat();return st.session_state.chats[0]


# CORRECTION — Historique persistant : au premier chargement de la
# session, on récupère les discussions déjà enregistrées sur disque au
# lieu de repartir d'une liste vide. La discussion la plus récemment
# mise à jour redevient la discussion active.
if "chats" not in st.session_state:
    st.session_state.chats = load_history()
if "active_id" not in st.session_state:
    if st.session_state.chats:
        st.session_state.active_id = sorted(
            st.session_state.chats,
            key=lambda c: c["updated_at"],
            reverse=True,
        )[0]["id"]
    else:
        new_chat()
if "active_documents" not in st.session_state: st.session_state.active_documents=[]
if "pending_ollama" not in st.session_state: st.session_state.pending_ollama=None
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

info=documents()
all_names=[x.get("name") for x in info if x.get("name")]
# Les documents déjà indexés sont seulement disponibles dans la liste.
# Ils ne sont PAS sélectionnés automatiquement.
# Seuls les nouveaux fichiers chargés pendant cette session sont ajoutés
# automatiquement à la sélection (voir les blocs d'upload ci-dessous).
st.session_state.active_documents=[
    x for x in st.session_state.active_documents
    if x in all_names
]

with st.sidebar:
    st.markdown('<div class="sidebar-logo">✦</div><div class="sidebar-title">ZTE AI LOCAL AGENT</div><div class="sidebar-subtitle">Intelligent Decision Assistant</div>',unsafe_allow_html=True)
    if st.button("＋ Nouvelle discussion",use_container_width=True):new_chat();save_history();st.rerun()
    search=st.text_input("Recherche",placeholder="Rechercher une discussion...",label_visibility="collapsed")
    st.markdown('<div class="sidebar-label">DISCUSSIONS RÉCENTES</div>',unsafe_allow_html=True)
    for c in sorted(st.session_state.chats,key=lambda x:x["updated_at"],reverse=True)[:10]:
        if search and search.lower() not in c["title"].lower():continue
        col_chat,col_del=st.columns([6,1])
        with col_chat:
            if st.button(("● " if c["id"]==st.session_state.active_id else "○ ")+c["title"],key="c"+c["id"],use_container_width=True):st.session_state.active_id=c["id"];st.rerun()
        with col_del:
            if st.button("🗑",key="del"+c["id"],use_container_width=True,help="Supprimer cette discussion"):delete_chat(c["id"]);st.rerun()

    st.markdown('<div class="sidebar-label">MÉMOIRE DOCUMENTAIRE</div>',unsafe_allow_html=True)
    if info:
        for x in info:
            st.markdown(f'<div class="doc-row"><span class="doc-icon">▧</span><span class="doc-name">{x.get("name")}</span><b class="doc-count">{x.get("chunks",0)}</b></div>',unsafe_allow_html=True)
    else: st.caption("Aucun document indexé.")

    st.markdown('<div class="sidebar-label">DOCUMENTS UTILISÉS</div>',unsafe_allow_html=True)
    st.session_state.active_documents=st.multiselect("Documents actifs",all_names,default=st.session_state.active_documents,label_visibility="collapsed")

    # CORRECTION — Retour au bouton Upload dans la sidebar (le "+" du
    # champ de saisie est retiré plus bas, il ne permettait pas
    # d'obtenir le comportement voulu). Même concept que prévu pour le
    # "+" : indexation silencieuse + ajout à "Documents utilisés" +
    # confirmation affichée dans la conversation, sans solliciter
    # l'agent pour une analyse automatique non demandée.
    # CORRECTION — Uploader réinitialisable :
    # après une indexation réussie, la clé change et Streamlit
    # crée un nouveau widget. Le fichier sélectionné est donc
    # retiré de l'état du file_uploader et le rerun ne relance
    # pas l'indexation en boucle.
    st.markdown('<div class="sidebar-label">AJOUTER UN DOCUMENT</div>',unsafe_allow_html=True)

    uploads=st.file_uploader(
        "Ajouter",
        type=["pdf","docx","doc","xlsx","xls","pptx","txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key=f"document_uploader_{st.session_state.uploader_key}"
    )

    if uploads:
        indexed_names=[]

        for u in uploads:
            ok,msg=index_upload(u)

            if ok:
                if u.name not in st.session_state.active_documents:
                    st.session_state.active_documents.append(u.name)
                indexed_names.append(u.name)
            else:
                st.error(msg)

        if indexed_names:
            noms=", ".join(indexed_names)

            confirmation=(
                f"📎 Fichier(s) indexé(s) et ajouté(s) à "
                f"« Documents utilisés » : {noms}. "
                f"Vous pouvez maintenant poser votre question."
            )

            target_chat=current_chat()
            target_chat["messages"].append({
                "role":"assistant",
                "content":confirmation,
                "sources":[]
            })
            target_chat["updated_at"]=datetime.now().isoformat()

            save_history()

            # Réinitialise le file_uploader avant le rerun.
            st.session_state.uploader_key += 1

            # Un seul rerun : le nouveau widget sera vide.
            st.rerun()

    if info:
        with st.expander("Supprimer de la mémoire"):
            for x in info:
                name=x.get("name")
                if st.button("🗑 "+name,key="d"+name,use_container_width=True):
                    ChromaIndexer().delete_document(name)
                    p=UPLOAD_DIR/name
                    if p.is_file():p.unlink()
                    st.session_state.active_documents=[n for n in st.session_state.active_documents if n!=name]
                    documents.clear();st.rerun()

st.markdown('<div class="topbar"><div class="topbar-brand"><span>ZTE</span> AI LOCAL AGENT</div><div class="topbar-right">Intelligent Decision Assistant</div></div>',unsafe_allow_html=True)
st.markdown('<div class="agent-hero"><div class="agent-badge">✦</div><h1>ZTE AI AGENT</h1><p>Votre assistant IA local pour analyser, rechercher et exploiter vos documents.</p><div class="agent-status"><strong><span class="status-dot"></span>Agent opérationnel</strong><span>·</span><span>Mémoire documentaire locale</span><span>·</span><span>Llama 3.2</span><span>·</span><span>ChromaDB</span></div></div>',unsafe_allow_html=True)
st.markdown('<div class="info-box">ⓘ Sans document sélectionné, Ollama répond directement. Avec des documents sélectionnés, l’agent utilise uniquement ces documents. Si l’information manque, il vous demande avant d’utiliser Ollama.</div>',unsafe_allow_html=True)

# CORRECTION — Bandeau d'état visible sur la sélection de documents :
# avant, rien n'indiquait clairement à l'utilisateur qu'aucun document
# n'était sélectionné, ce qui menait à des réponses du type "je n'ai
# pas accès aux fichiers" sans que la cause soit évidente. On affiche
# maintenant l'état actuel juste au-dessus de la conversation.
if st.session_state.active_documents:
    noms=", ".join(st.session_state.active_documents)
    st.markdown(f'<div class="info-box" style="border-color:rgba(50,211,154,.35);background:rgba(50,211,154,.08);color:#b8f2da">📎 Document(s) actif(s) : {noms}</div>',unsafe_allow_html=True)
else:
    st.markdown('<div class="info-box" style="border-color:rgba(253,176,34,.4);background:rgba(253,176,34,.1);color:#ffdca8">⚠️ Aucun document sélectionné — vos questions seront traitées uniquement avec les connaissances générales d\'Ollama. Sélectionnez un document dans « Documents utilisés » (sidebar) si vous voulez interroger un fichier.</div>',unsafe_allow_html=True)

chat=current_chat()
for m in chat["messages"]:
    with st.chat_message(m["role"],avatar="👤" if m["role"]=="user" else "🤖"):
        st.markdown(m["content"])
        if m.get("sources"):st.caption("Sources : "+" · ".join(m["sources"]))

pending=st.session_state.pending_ollama
if pending:
    st.warning("Je ne trouve pas cette information dans les documents sélectionnés.")
    st.write("Voulez-vous utiliser Ollama pour répondre avec ses connaissances générales ?")
    a,b=st.columns(2)
    if a.button("🤖 Oui, utiliser Ollama",key="yes_ollama",use_container_width=True):
        with st.chat_message("assistant",avatar="🤖"):
            with st.spinner("Ollama réfléchit..."):
                r=load_agent().process(pending["query"],pending["documents"],force_ollama=True)
            st.markdown(r["answer"])
        chat["messages"].append({"role":"assistant","content":r["answer"],"sources":[]})
        chat["updated_at"]=datetime.now().isoformat()
        st.session_state.pending_ollama=None;save_history();st.rerun()
    if b.button("Non, rester sur les documents",key="no_ollama",use_container_width=True):
        answer="D’accord. Je reste limité aux documents sélectionnés."
        with st.chat_message("assistant",avatar="🤖"):st.markdown(answer)
        chat["messages"].append({"role":"assistant","content":answer,"sources":[]})
        chat["updated_at"]=datetime.now().isoformat()
        st.session_state.pending_ollama=None;save_history();st.rerun()

# CORRECTION — Le "+" (accept_file) est retiré : il ne permettait pas
# vraiment d'indexer un fichier avant de taper le texte (Streamlit ne
# renvoie les fichiers attachés qu'au moment de l'envoi complet). Le
# même concept (indexer + confirmer avant de poser la question) est
# maintenant géré par le bouton Upload de la sidebar à la place.
value=st.chat_input("Écrivez votre message…")

if value:
    question=str(value).strip()
    if not question:question="Analyse les documents que je viens de charger."

    chat["messages"].append({"role":"user","content":question})
    if len(chat["messages"])==1:chat["title"]=generate_conversation_title(question,st.session_state.active_documents)
    chat["updated_at"]=datetime.now().isoformat()
    save_history()

    with st.chat_message("assistant",avatar="🤖"):
        with st.spinner("Analyse en cours..."):
            try:
                r=load_agent().process(question,st.session_state.active_documents)
                # CORRECTION : on déclenche aussi la demande Ollama quand des
                # documents sont sélectionnés et que la réponse ressemble à
                # une non-réponse, même si needs_ollama n'a pas été renvoyé.
                triggers_ollama_question = r.get("needs_ollama") or (
                    bool(st.session_state.active_documents)
                    and answer_not_found(r.get("answer"))
                )
                if triggers_ollama_question:
                    st.markdown(r["answer"])
                    st.session_state.pending_ollama={"query":question,"documents":r.get("document_names",st.session_state.active_documents)}
                else:
                    st.markdown(r["answer"])
                    chat["messages"].append({"role":"assistant","content":r["answer"],"sources":r.get("sources",[])})
                    chat["updated_at"]=datetime.now().isoformat()
            except Exception as exc:
                st.error(f"Une erreur est survenue : {exc}")
    save_history()
    st.rerun()

st.markdown('<div class="footer">ZTE AI LOCAL AGENT · Llama 3.2 · ChromaDB · Données locales</div>',unsafe_allow_html=True)