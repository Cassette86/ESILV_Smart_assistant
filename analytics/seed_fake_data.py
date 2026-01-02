import random
from datetime import datetime, timedelta
from db import get_db

# ==============================
# PARAMÈTRES
# ==============================

NB_USERS = 25
NB_DAYS = 30
AVG_QUERIES_PER_DAY = 12

THEMES = [
    "Admissions",
    "Programs",
    "Student life",
    "Careers",
    "Research",
    "Other"
]

DOCUMENTS = [
    "ingenieur_data_science.txt",
    "admissions_esilv.txt",
    "student_life.txt",
    "careers_after_esilv.txt",
    "research_labs.txt",
    "campus_nanterre.txt",
]

# ==============================
# UTILS
# ==============================

def random_timestamp(days_back):
    now = datetime.now()
    delta = timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    return (now - delta).isoformat(timespec="seconds")


# ==============================
# SEED INTERACTIONS
# ==============================

def seed_interactions():
    conn = get_db()
    cur = conn.cursor()

    interactions = []

    for _ in range(NB_DAYS * AVG_QUERIES_PER_DAY):
        user_id = f"user_{random.randint(1, NB_USERS)}"
        session_id = f"session_{random.randint(1, 200)}"

        email_clicked = random.random() < 0.15
        conversion = email_clicked and random.random() < 0.35

        interactions.append((
            random_timestamp(NB_DAYS),
            user_id,
            session_id,
            random.choice(THEMES),
            random.choice(DOCUMENTS),
            round(random.uniform(0.25, 0.95), 3),
            int(email_clicked),
            int(conversion),
        ))

    cur.executemany("""
        INSERT INTO interactions (
            timestamp,
            user_id,
            session_id,
            theme,
            used_sources,
            max_similarity,
            email_clicked,
            conversion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, interactions)

    conn.commit()
    conn.close()
    print(f"✅ Inserted {len(interactions)} fake interactions")


# ==============================
# SEED LEADS (VERSION SAFE)
# ==============================

def seed_fake_leads(n=15):
    conn = get_db()
    cur = conn.cursor()

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

    leads = []
    for i in range(n):
        leads.append((
            datetime.now().isoformat(timespec="seconds"),
            f"user_{random.randint(1, NB_USERS)}",
            f"User{i}",
            "Demo",
            f"user{i}@example.com",
            random.choice(["L1", "L2", "L3", "M1", "M2"]),
            random.choice(["Data", "AI", "Finance", "Engineering"]),
            1,
            random.randint(0, 1)
        ))

    cur.executemany("""
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
    """, leads)

    conn.commit()
    conn.close()
    print(f"✅ Inserted {n} fake leads")


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    seed_interactions()
    seed_fake_leads()
