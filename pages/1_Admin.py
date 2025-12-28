import streamlit as st

st.set_page_config(
    page_title="Admin – ESILV Chatbot",
    layout="wide"
)

# =========================
# 1. HEADER / TITRE
# =========================
st.title("Chatbot ESILV - Analytics Dashboard")
st.divider()

# =========================
# 2. BARRE D’ACTIONS (3 boutons)
# =========================
action_col1, action_col2, action_col3, _ = st.columns([1.2, 1, 1, 5])

with action_col1:
    date_range = st.selectbox(
        "Date Range",
        ["Weekly", "Monthly", "Quarterly", "Yearly"],
        label_visibility="collapsed"
    )

with action_col2:
    st.button("Report 📥")

with action_col3:
    st.button("🔄")

st.divider()

# =========================
# 3. KPI CARDS (ligne de cards)
# =========================
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric("Users", "1 248", "+12%")

with kpi2:
    st.metric("Queries", "3 502", "+5%")

with kpi3:
    st.metric("Sessions", "18 430", "+9%")

with kpi4:
    st.metric("Emails", "820", "-4%")

with kpi5:
    st.metric("Conversions", "0", "0")

st.divider()

# =========================
# 4. ZONE PRINCIPALE (GRILLE 2x2)
# =========================
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    st.subheader("Queries theme")
    st.info("Chart placeholder")
    # ex: st.line_chart(data)

with row1_col2:
    st.subheader("Usage over time")
    st.info("Chart placeholder")

with row2_col1:
    st.subheader("Content Coverage")
    st.write("Coverage score :")
    st.info("Chart placeholder")
    st.write("Top used documents :")
    st.info("List placeholder")
    st.write("Underused documents :")
    st.info("List placeholder")

with row2_col2:
    st.subheader("Conversion Funnel")
    st.info("Chart placeholder")