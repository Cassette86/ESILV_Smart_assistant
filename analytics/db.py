import sqlite3
import os

DB_PATH = "data/analytics/analytics.db"

def get_db():
    os.makedirs("data/analytics", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        week INTEGER,
        month INTEGER,
        user_id TEXT,
        session_id TEXT,
        query TEXT,
        query_length INTEGER,
        theme TEXT,
        confidence_score REAL,
        retrieved_docs INTEGER,
        avg_similarity REAL,
        max_similarity REAL,
        response_length INTEGER,
        used_sources TEXT,
        email_clicked BOOLEAN,
        conversion BOOLEAN
    )
    """)

    conn.commit()
    conn.close()