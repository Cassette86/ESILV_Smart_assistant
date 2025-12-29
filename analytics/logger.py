from datetime import datetime
from analytics.db import get_db

def log_interaction(
    user_id,
    session_id,
    query,
    theme,
    rag_results,
    response,
    email_clicked=False,
    conversion=False
):
    conn = get_db()
    cur = conn.cursor()

    ts = datetime.now()

    cur.execute("""
        INSERT INTO interactions VALUES (
            NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        ts,
        ts.isocalendar()[1],
        ts.month,
        user_id,
        session_id,
        query,
        len(query),
        theme,
        max(rag_results["similarities"]),
        len(rag_results["similarities"]),
        sum(rag_results["similarities"]) / len(rag_results["similarities"]),
        max(rag_results["similarities"]),
        len(response),
        ",".join(rag_results["sources"]),
        email_clicked,
        conversion
    ))

    conn.commit()
    conn.close()
