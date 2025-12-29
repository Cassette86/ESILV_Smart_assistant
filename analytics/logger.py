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

    # --- SAFE METRICS ---
    similarity_count = len(similarities)
    max_similarity = max(similarities) if similarities else None
    avg_similarity = (
        sum(similarities) / similarity_count
        if similarity_count > 0
        else None
    )

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
        max_similarity,             # SAFE
        similarity_count,
        avg_similarity,             # SAFE
        max_similarity,             # SAFE (si tu veux la garder deux fois)
        len(response),
        ",".join(sources) if sources else None,
        email_clicked,
        conversion
    ))

    conn.commit()
    conn.close()
