import csv
import os
from datetime import datetime

from analytics.metrics import (
    users_kpi,
    queries_kpi,
    sessions_kpi,
    emails_kpi,
    conversions_kpi,
    queries_by_theme,
    coverage_score,
    top_used_documents,
    underused_documents
)

REPORT_DIR = "data/reports"


def generate_report(period="weekly"):
    os.makedirs(REPORT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"chatbot_report_{period}_{timestamp}.csv"
    filepath = os.path.join(REPORT_DIR, filename)

    # ================= KPIs =================
    users, users_var = users_kpi(period)
    queries, queries_var = queries_kpi(period)
    sessions, sessions_var = sessions_kpi(period)
    emails, emails_var = emails_kpi(period)
    convs, convs_var = conversions_kpi(period)

    # ================= Other metrics =================
    themes = queries_by_theme(period)
    coverage = coverage_score(period)
    top_docs = top_used_documents(period=period)
    under_docs = underused_documents(period=period)

    # ================= Write CSV =================
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["ESILV Chatbot – Analytics Report"])
        writer.writerow(["Generated at", datetime.now().isoformat()])
        writer.writerow(["Period", period])
        writer.writerow([])

        writer.writerow(["KPI", "Value", "Variation (%)"])
        writer.writerow(["Users", users, users_var])
        writer.writerow(["Queries", queries, queries_var])
        writer.writerow(["Sessions", sessions, sessions_var])
        writer.writerow(["Emails", emails, emails_var])
        writer.writerow(["Conversions", convs, convs_var])
        writer.writerow([])

        writer.writerow(["Coverage score", coverage])
        writer.writerow([])

        writer.writerow(["Queries by theme"])
        writer.writerow(["Theme", "Count"])
        for theme, count in themes:
            writer.writerow([theme, count])
        writer.writerow([])

        writer.writerow(["Top used documents"])
        writer.writerow(["Document", "Usage count"])
        for doc, count in top_docs:
            writer.writerow([doc, count])
        writer.writerow([])

        writer.writerow(["Underused documents"])
        for doc in under_docs:
            writer.writerow([doc])

    return filepath
