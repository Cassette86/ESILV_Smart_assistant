import streamlit as st
import base64

st.set_page_config(page_title="ESILV Chatbot", layout="centered")

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

# ================== HEADER ==================
st.markdown(f"""
<div class="chat-header">
    <div class="header-left">
        <img src="data:image/png;base64,{logo_base64}" />
        <div class="header-title">ESILV Chatbot</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================== MESSAGES + INPUT ==================
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

# input (UN SEUL FORMULAIRE)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Posez votre question…")
    sent = st.form_submit_button("➜")

st.markdown('</div>', unsafe_allow_html=True)

# ================== LOGIC ==================
if sent and user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    })
    st.rerun()
