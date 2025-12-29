from datetime import datetime
from analytics.db import get_db

def save_lead(
    user_id,
    first_name,
    last_name,
    email,
    level,
    interests,
    consent,
    newsletter
):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO leads (
            timestamp,
            user_id,
            first_name,
            last_name,
            email,
            level,
            interests,
            consent,
            newsletter
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(),
        user_id,
        first_name,
        last_name,
        email,
        level,
        ",".join(interests),  # simple et suffisant
        consent,
        newsletter
    ))

    conn.commit()
    conn.close()
