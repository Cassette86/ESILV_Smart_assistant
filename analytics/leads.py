from analytics.db import get_db
from datetime import datetime

def save_lead(
    user_id,
    first_name,
    last_name,
    email,
    study_level,
    interests,
    consent,
    newsletter
):
    conn = get_db()
    cur = conn.cursor()

    # sécurité : table existante
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            user_id TEXT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            study_level TEXT,
            interests TEXT,
            consent INTEGER NOT NULL,
            newsletter INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        INSERT INTO leads (
            created_at,
            user_id,
            first_name,
            last_name,
            email,
            study_level,
            interests,
            consent,
            newsletter
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(timespec="seconds"),
        user_id,
        first_name,
        last_name,
        email,
        study_level,
        interests,
        int(consent),
        int(newsletter)
    ))

    conn.commit()
    conn.close()
