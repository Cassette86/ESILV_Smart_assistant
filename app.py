import streamlit as st
import base64 # for image encoding
from rag.service import answer_with_rag
import uuid
#================== ANALYTICS ==================
from analytics.db import init_db
from analytics.logger import log_interaction
from analytics.themes import detect_theme
from analytics.leads import save_lead
from agents.orchestrator import orchestrate

init_db()

if "mode" not in st.session_state:
    st.session_state.mode = "chat"

if "contact_data" not in st.session_state:
    st.session_state.contact_data = {}

st.set_page_config(page_title="ESILV Chatbot", layout="centered")

# ================== IMAGE TO BASE64 ==================
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = img_to_base64("assets/chatbot_head.png")

# ================== CSS ==================
st.markdown("""
<style>
.stApp {
    background: #FFFFFF;
}

/* -------- Header -------- */
.chat-header { 
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    border-bottom: 1px solid #eee;
    margin-bottom: 12px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 8px;
}

.header-left img {
    width: 28px;
    height: 28px;
}

.header-title {
    font-size: 14px;
    font-weight: 600;
    color: #E6007E;
}

/* -------- Messages -------- */
.chat-wrapper {
    max-width: 720px;   /* ajuste : 600 / 680 / 720 */
    margin: auto;
}            

.chat-messages {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 16px;
}

.msg-user {
    background: #FFFFFF;
    align-self: flex-end;
    margin-left: auto;
    text-align: right;
    border-radius: 16px 16px 4px 16px;
    padding: 8px 12px;
    max-width: 70%;
}

.msg-bot {
    background: #F1E9F5;
    align-self: flex-start;
    margin-right: auto;
    text-align: left;
    border-radius: 16px 16px 16px 4px;
    padding: 8px 12px;
    max-width: 70%;
}

/* -------- Input -------- */
.stTextInput > div > div > input {
    border-radius: 14px;
    padding: 10px 12px;
}

.stButton > button {
    border-radius: 12px;
    height: 42px;
}
</style>
""", unsafe_allow_html=True)

# ================== STATE ==================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================== USER / SESSION IDS ==================
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ================== HEADER ==================
st.markdown(f"""
<div class="chat-header">
    <div class="header-left">
        <img src="data:image/png;base64,{logo_base64}" />
        <div class="header-title">ESILV Chatbot</div>
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.mode == "chat":
    if st.button("📩 Je souhaite être recontacté"):
        st.session_state.mode = "contact"
        st.rerun()

def show_chat():
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

    # messages
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        cls = "msg-user" if msg["role"] == "user" else "msg-bot"
        st.markdown(
            f'<div class="{cls}">{msg["content"]}</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("", placeholder="Posez votre question…")
        sent = st.form_submit_button("➜")

    st.markdown('</div>', unsafe_allow_html=True)

    # ========== LOGIC ==========
    if sent and user_input:
        # 1️⃣ message user
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        # 2️⃣ ORCHESTRATION
        decision = orchestrate(user_input, st.session_state)
        st.session_state.last_intent = decision["intent"]

        # 3️⃣ ACTIONS SELON L’INTENT
        if decision["action"] == "switch_to_contact":
            st.session_state.mode = "contact"
            st.rerun()

        if decision["action"] == "ask_clarification":
            st.session_state.messages.append({
                "role": "assistant",
                "content": decision["message"]
            })
            st.rerun()

        # 4️⃣ SINON → RAG (factuel)
        with st.spinner("Recherche dans les documents ESILV..."):
            result = answer_with_rag(user_input)

        answer = result["answer"]   # ✅ FIX

        theme = detect_theme(user_input)
        rag_results = {
            "similarities": result.get("similarities", []),
            "sources": result.get("sources", [])
        }
        log_interaction(
            user_id=st.session_state.user_id,
            session_id=st.session_state.session_id,
            query=user_input,
            theme=theme,
            rag_results=rag_results,
            response=answer
        )

        if result["sources"]:
            answer += "<br><br><small><b>Sources :</b><br>"
            for s in result["sources"]:
                answer += f"- {s}<br>"
            answer += "</small>"

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()


def show_contact_form():
    st.button("⬅️ Retour à la discussion",
              on_click=lambda: st.session_state.update({"mode": "chat"}))

    st.subheader("📩 Demande de contact")

    # Niveau
    level = st.radio(
        "Niveau d’étude",
        ["L1", "L2", "L3", "M1", "M2", "Autre"],
        horizontal=True
    )

    # Identité
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("Prénom")
    with col2:
        last_name = st.text_input("Nom")

    email = st.text_input("Email")

    interests = st.multiselect(
        "Domaines d’intérêt (facultatif)",
        [
            "IA", "Data", "Cybersécurité",
            "Finance", "Industrie", "International"
        ]
    )

    consent = st.checkbox(
        "J’accepte que mes données soient utilisées pour être recontacté(e) (obligatoire)"
    )

    newsletter = st.checkbox(
        "Je souhaite recevoir la newsletter ESILV (facultatif)"
    )

    if st.button("Envoyer ma demande"):
        if not consent:
            st.error("Le consentement est obligatoire.")
        elif not email or not first_name or not last_name:
            st.error("Merci de remplir tous les champs obligatoires.")
        else:
            save_lead(
                user_id=st.session_state.user_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                level=level,
                interests=interests,
                consent=consent,
                newsletter=newsletter
            )

            st.success("Votre demande a bien été envoyée. Nous vous recontacterons.")
            st.session_state.mode = "chat"
            st.rerun()
