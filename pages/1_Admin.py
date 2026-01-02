import streamlit as st
import os

from analytics.report import generate_report

from analytics.metrics import (
    users_kpi,
    queries_kpi,
    sessions_kpi,
    emails_kpi,
    conversions_kpi,
    queries_by_theme,
    usage_over_time,
    coverage_score,
    top_used_documents,
    underused_documents,
    users_count, 
    queries_count,
    conversions_count
)

st.set_page_config(
    page_title="Admin – ESILV Chatbot",
    layout="wide"
)

if "show_upload" not in st.session_state:
    st.session_state.show_upload = False

# =========================Title and Header =========================
st.title("Chatbot ESILV - Analytics Dashboard")
st.divider()

# =========================Action Buttons =========================
action_col1, action_col2, action_col3, action_col4, _ = st.columns([1.2, 1, 1, 1, 2])

with action_col1:
    date_range = st.selectbox(
        "Date Range",
        ["Weekly", "Monthly", "Quarterly", "Yearly"],
        label_visibility="collapsed"
    )
period = date_range.lower()

with action_col2:
    if st.button("Report 📥"):
        path = generate_report(period)
        st.success("Report generated")
        st.download_button(
            label="Download report",
            data=open(path, "rb"),
            file_name=path.split("/")[-1],
            mime="text/csv"
        )


with action_col3:
    if st.button("🔄"):
        st.rerun()

with action_col4:
    if st.button("📄 Load Data"):
        st.session_state.show_upload = not st.session_state.show_upload

with action_col4:
    if st.session_state.show_upload:
        st.markdown("Upload a document (PDF, TXT)")

        uploaded_file = st.file_uploader(
            " ",
            type=["pdf", "txt"],
            key="kb_uploader"
        )

        if st.button("Load Data 🔄"):
            if uploaded_file is None:
                st.warning("Please upload a file first.")
            else:
                os.makedirs("data/raw/brochures", exist_ok=True)

                file_path = os.path.join(
                    "data/raw/brochures",
                    uploaded_file.name
                )

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.success(f"Document '{uploaded_file.name}' uploaded successfully.")
                st.info("Run the ingestion pipeline to make it available to the chatbot.")


st.divider()

# =========================KPIs cards =========================
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

users_value, users_var = users_kpi(period)
queries_value, queries_var = queries_kpi(period)
sessions_value, sessions_var = sessions_kpi(period)
emails_value, emails_var = emails_kpi(period)
conv_value, conv_var = conversions_kpi(period)

with kpi1:
    st.metric("Users", users_value, f"{users_var:+.1f}%" if users_var else "N/A")

with kpi2:
    st.metric("Queries", queries_value, f"{queries_var:+.1f}%" if queries_var else "N/A")

with kpi3:
    st.metric("Sessions", sessions_value, f"{sessions_var:+.1f}%" if sessions_var else "N/A")

with kpi4:
    st.metric("Emails", emails_value, f"{emails_var:+.1f}%" if emails_var else "N/A")

with kpi5:
    st.metric("Conversions", conv_value, f"{conv_var:+.1f}%" if conv_var else "N/A")


st.divider()

# ========================= Charts and Data =========================
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    st.subheader("Queries theme")

    data = queries_by_theme(period)

    if data:
        st.bar_chart(
            {theme: count for theme, count in data}
        )
    else:
        st.info("No data available")

with row1_col2:
    st.subheader("Usage over time")

    data = usage_over_time(period)

    if data:
        st.line_chart(data)
    else:
        st.info("No data available")

with row2_col1:
    st.subheader("Content Coverage")

    score = coverage_score(period)

    st.metric("Coverage score", f"{score:.2f}")

    st.write("Top used documents")

    top_docs = top_used_documents(period=period)

    for doc, count in top_docs:
        st.write(f"- {doc} ({count})")

    st.write("Underused documents")

    underused = underused_documents(period=period)

    for doc in underused:
        st.write(f"- {doc}")

with row2_col2:
    st.subheader("Conversion Funnel")

    funnel = {
        "Users": users_count(period),
        "Queries": queries_count(period),
        "Conversions": conversions_count(period)
    }

    st.bar_chart(funnel)