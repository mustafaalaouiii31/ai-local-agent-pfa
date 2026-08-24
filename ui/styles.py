"""Professional ZTE theme for the Streamlit local AI agent."""

THEME_CSS = """
<style>

:root {
    --zte-blue: #0066FF;
    --zte-blue-dark: #0047B3;
    --zte-blue-light: #EAF2FF;

    --navy: #071A3A;
    --navy-2: #0B2452;
    --navy-3: #102E63;

    --white: #FFFFFF;

    /* CORRECTION : le fond de toute la page reprend maintenant le
       même bleu marine que la sidebar (au lieu du gris clair
       d'origine). Les couleurs de texte / bordures ci-dessous sont
       adaptées en conséquence pour rester lisibles sur fond foncé. */
    --background: var(--navy);
    --surface: var(--navy-2);

    --text: #E8EFFC;
    --muted: #9EB4D8;
    --line: #1C477D;

    --success: #12B76A;
}

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background: var(--background);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.4rem;
    padding-bottom: 7rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background: var(--navy);
    border-right: 1px solid #18345F;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.2rem 1rem;
}


/* Logo */

.sidebar-logo {
    width: 42px;
    height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 12px;

    background: var(--zte-blue);

    color: white;

    font-size: 22px;
    font-weight: 800;

    margin-bottom: 10px;

    box-shadow: 0 8px 20px rgba(0, 102, 255, 0.25);
}


.sidebar-title {
    color: white;

    font-size: 16px;
    font-weight: 800;

    letter-spacing: -0.02em;

    margin-bottom: 3px;
}


.sidebar-subtitle {
    color: #9EB4D8;

    font-size: 11px;

    margin-bottom: 25px;
}


/* Section */

.sidebar-section {
    color: #8EA8D1;

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 0.09em;

    margin-top: 24px;
    margin-bottom: 9px;
}


/* Search */

[data-testid="stSidebar"] input {
    background: #0C2855 !important;

    border: 1px solid #214574 !important;

    color: white !important;

    border-radius: 9px !important;
}

[data-testid="stSidebar"] input::placeholder {
    color: #829BC0 !important;
}


/* Buttons */

[data-testid="stSidebar"] .stButton > button {
    width: 100%;

    background: transparent;

    border: 1px solid transparent;

    color: #D8E4F7;

    border-radius: 8px;

    text-align: left;

    justify-content: flex-start;

    padding: 0.55rem 0.65rem;

    font-size: 0.82rem;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #102E63;

    border-color: #1C477D;

    color: white;
}


/* New conversation */

.new-chat-button button {
    background: var(--zte-blue) !important;

    color: white !important;

    border: none !important;

    justify-content: center !important;

    font-weight: 700 !important;
}


/* Documents */

.doc-row {
    display: flex;

    align-items: center;

    gap: 8px;

    padding: 8px 5px;

    border-bottom: 1px solid #16345E;

    color: #D8E4F7;

    font-size: 0.78rem;
}

.doc-icon {
    color: #70A9FF;

    font-size: 15px;

    flex-shrink: 0;
}

.doc-name {
    flex: 1;

    overflow: hidden;

    text-overflow: ellipsis;

    white-space: nowrap;
}

.doc-count {
    color: #8EA8D1;

    font-size: 0.7rem;
}


/* File uploader */

[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: #0A2147;

    border: 1px dashed #315B91;

    border-radius: 10px;

    padding: 5px;
}


/* Sidebar captions */

[data-testid="stSidebar"] .stCaption {
    color: #91A8CA !important;
}


/* ============================================================
   TOP BAR
   ============================================================ */

.topbar {
    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 0 0 14px 0;

    border-bottom: 1px solid var(--line);

    margin-bottom: 40px;
}


.topbar-brand {
    color: var(--text);

    font-size: 16px;

    font-weight: 800;

    letter-spacing: -0.02em;
}

.topbar-brand span {
    color: #70A9FF;
}


.topbar-right {
    color: var(--muted);

    font-size: 12px;
}


/* ============================================================
   HERO
   ============================================================ */

.agent-welcome {
    text-align: center;

    margin-bottom: 28px;
}


.agent-badge {
    width: 62px;
    height: 62px;

    margin: auto;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 18px;

    background: linear-gradient(
        135deg,
        #0066FF,
        #0047B3
    );

    color: white;

    font-size: 28px;

    font-weight: 800;

    box-shadow:
        0 12px 28px rgba(0, 102, 255, 0.24);
}


.agent-welcome h1 {
    color: var(--text);

    font-size: 28px;

    font-weight: 800;

    letter-spacing: -0.035em;

    margin-top: 13px;

    margin-bottom: 5px;
}


.agent-welcome p {
    color: var(--muted);

    font-size: 14px;

    margin: 0;
}


/* ============================================================
   STATUS
   ============================================================ */

.agent-status {
    display: flex;

    justify-content: center;

    align-items: center;

    gap: 9px;

    color: var(--muted);

    font-size: 12px;

    margin-bottom: 25px;
}


.status-dot {
    display: inline-block;

    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: var(--success);

    margin-right: 5px;

    box-shadow:
        0 0 0 3px rgba(18, 183, 106, 0.12);
}


/* ============================================================
   INFO BOX
   ============================================================ */

.info-box {
    display: flex;

    gap: 10px;

    align-items: flex-start;

    background: rgba(0, 102, 255, 0.14);

    border: 1px solid rgba(112, 169, 255, 0.35);

    color: #C9DCFF;

    border-radius: 10px;

    padding: 12px 15px;

    font-size: 12px;

    margin-bottom: 28px;
}


.info-icon {
    color: #70A9FF;

    font-size: 16px;

    font-weight: 700;
}


/* ============================================================
   CONVERSATION
   ============================================================ */

.conversation-header {
    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 15px;
}


.conversation-title {
    color: var(--text);

    font-size: 17px;

    font-weight: 800;
}


/* ============================================================
   CHAT
   ============================================================ */

[data-testid="stChatMessage"] {
    border-radius: 14px;

    border: 1px solid var(--line);

    background: var(--surface);

    margin-bottom: 10px;

    padding: 5px 8px;

    box-shadow:
        0 2px 7px rgba(0, 0, 0, 0.15);
}


[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: var(--text);

    line-height: 1.65;
}


/* User message */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: var(--navy-3);

    border-color: #2A5490;
}


/* Assistant */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: var(--surface);
}


/* ============================================================
   CHAT INPUT
   ============================================================ */

/* CORRECTION : le champ de saisie flottant en bas de page vit dans
   un conteneur fixe propre à Streamlit (stBottom /
   stBottomBlockContainer), distinct de .stApp. Sans le cibler
   explicitement, ce conteneur garde le fond sombre par défaut de
   Streamlit (quasi noir) au lieu du bleu marine du reste de la page. */

[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {
    background: var(--navy) !important;
}

[data-testid="stBottom"] > div {
    background: var(--navy) !important;
}

[data-testid="stChatInput"] {
    background: var(--surface);

    border: 1px solid var(--line);

    border-radius: 14px;

    box-shadow:
        0 5px 20px rgba(0, 0, 0, 0.25);
}


[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--muted) !important;
}


/* ============================================================
   SOURCES
   ============================================================ */

.source-note {
    color: var(--muted);

    font-size: 11px;

    margin-top: -4px;
}


/* ============================================================
   WEB SEARCH
   ============================================================ */

.web-search-box {
    background: var(--surface);

    border: 1px solid var(--line);

    border-radius: 10px;

    padding: 12px;

    margin-top: 8px;

    color: var(--text);
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;

    color: var(--muted);

    font-size: 10px;

    padding-top: 30px;
}


/* ============================================================
   GENERAL BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 9px;

    border: 1px solid var(--line);

    background: var(--surface);

    color: var(--text);

    font-weight: 600;
}


.stButton > button:hover {
    border-color: #70A9FF;

    color: #70A9FF;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .agent-welcome h1 {
        font-size: 23px;
    }

    .agent-status {
        flex-wrap: wrap;
    }

}

</style>
"""