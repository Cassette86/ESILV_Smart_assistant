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

def init_leads_table():
    conn = get_db()
    cur = conn.cursor()

    # création de la table (nouvelle DB)
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

    # migration : ajout user_id si table déjà existante
    cur.execute("PRAGMA table_info(leads)")
    columns = [row[1] for row in cur.fetchall()]

    if "user_id" not in columns:
        cur.execute("ALTER TABLE leads ADD COLUMN user_id TEXT")

    conn.commit()
    conn.close()
