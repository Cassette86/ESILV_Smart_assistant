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

    similarities = rag_results.get("similarities", [])
    sources = rag_results.get("sources", [])

    retrieved_docs = len(sources) if sources else 0

    max_similarity = max(similarities) if similarities else None
    avg_similarity = (
        sum(similarities) / len(similarities)
        if similarities else None
    )
    confidence_score = max_similarity

    cur.execute("""
        INSERT INTO interactions VALUES (
            NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        ts,                         # timestamp
        ts.isocalendar()[1],        # week
        ts.month,                   # month
        user_id,
        session_id,
        query,
        len(query),
        theme,
        confidence_score,
        retrieved_docs,
        avg_similarity,
        max_similarity,          # SAFE (si tu veux la garder deux fois)
        len(response),
        ",".join(sources) if sources else None,
        email_clicked,
        conversion
    ))

    conn.commit()
    conn.close()
