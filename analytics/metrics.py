from analytics.db import get_db
from datetime import datetime

# =========================================================
# Helpers
# =========================================================

def _period_filter(period: str):
    """
    Returns SQL WHERE clause fragment based on selected period
    """
    if period == "weekly":
        return "WHERE timestamp >= date('now', '-7 days')"
    if period == "monthly":
        return "WHERE timestamp >= date('now', '-30 days')"
    if period == "quarterly":
        return "WHERE timestamp >= date('now', '-90 days')"
    if period == "yearly":
        return "WHERE timestamp >= date('now', '-365 days')"
    return ""


# =========================================================
# KPI COUNTERS (Top cards)
# =========================================================

def users_count(period):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(DISTINCT user_id)
        FROM interactions
        {_period_filter(period)}
    """)
    value = cur.fetchone()[0]
    conn.close()
    return value


def queries_count(period):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(*)
        FROM interactions
        {_period_filter(period)}
    """)
    value = cur.fetchone()[0]
    conn.close()
    return value


def sessions_count(period):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(DISTINCT session_id)
        FROM interactions
        {_period_filter(period)}
    """)
    value = cur.fetchone()[0]
    conn.close()
    return value


def emails_count(period):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(*)
        FROM interactions
        {_period_filter(period)}
        AND email_clicked = 1
    """)
    value = cur.fetchone()[0]
    conn.close()
    return value


def conversions_count(period):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(*)
        FROM interactions
        {_period_filter(period)}
        AND conversion = 1
    """)
    value = cur.fetchone()[0]
    conn.close()
    return value


# =========================================================
# QUERIES THEME
# =========================================================

def queries_by_theme(period):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT theme, COUNT(*) as count
        FROM interactions
        {_period_filter(period)}
        GROUP BY theme
        ORDER BY count DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


# =========================================================
# USAGE OVER TIME
# =========================================================

def usage_over_time(period):
    conn = get_db()
    cur = conn.cursor()

    if period == "weekly":
        group_by = "date(timestamp)"
    elif period == "monthly":
        group_by = "strftime('%Y-%W', timestamp)"
    elif period == "yearly":
        group_by = "strftime('%Y-%m', timestamp)"
    else:
        group_by = "date(timestamp)"

    cur.execute(f"""
        SELECT {group_by} as time_unit, COUNT(*)
        FROM interactions
        {_period_filter(period)}
        GROUP BY time_unit
        ORDER BY time_unit
    """)

    rows = cur.fetchall()
    conn.close()

    # Streamlit-friendly format
    return {row[0]: row[1] for row in rows}


# =========================================================
# CONTENT COVERAGE
# =========================================================

def coverage_score(period):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT AVG(max_similarity)
        FROM interactions
        {_period_filter(period)}
    """)
    value = cur.fetchone()[0]
    conn.close()
    return round(value, 3) if value else 0.0


def top_used_documents(period, limit=5):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT used_sources, COUNT(*) as count
        FROM interactions
        {_period_filter(period)}
        GROUP BY used_sources
        ORDER BY count DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


def underused_documents(period, limit=5):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT used_sources, COUNT(*) as count
        FROM interactions
        {_period_filter(period)}
        GROUP BY used_sources
        ORDER BY count ASC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]

# ======================Variations ====================================

def _previous_period(period: str):
    if period == "weekly":
        return "WHERE timestamp BETWEEN date('now', '-14 days') AND date('now', '-7 days')"
    if period == "monthly":
        return "WHERE timestamp BETWEEN date('now', '-60 days') AND date('now', '-30 days')"
    if period == "quarterly":
        return "WHERE timestamp BETWEEN date('now', '-180 days') AND date('now', '-90 days')"
    if period == "yearly":
        return "WHERE timestamp BETWEEN date('now', '-730 days') AND date('now', '-365 days')"
    return ""

def metric_with_variation(
    query_sql: str,
    period="weekly"
):
    conn = get_db()
    cur = conn.cursor()

    # valeur actuelle
    cur.execute(f"""
        {query_sql}
        {_period_filter(period)}
    """)
    current = cur.fetchone()[0] or 0

    # valeur précédente
    cur.execute(f"""
        {query_sql}
        {_previous_period(period)}
    """)
    previous = cur.fetchone()[0] or 0

    conn.close()

    # calcul variation
    if previous == 0:
        variation = None
    else:
        variation = round(((current - previous) / previous) * 100, 1)

    return current, variation

def users_kpi(period="weekly"):
    return metric_with_variation(
        "SELECT COUNT(DISTINCT user_id) FROM interactions",
        period
    )

def queries_kpi(period="weekly"):
    return metric_with_variation(
        "SELECT COUNT(*) FROM interactions",
        period
    )

def sessions_kpi(period="weekly"):
    return metric_with_variation(
        "SELECT COUNT(DISTINCT session_id) FROM interactions",
        period
    )

def emails_kpi(period="weekly"):
    return metric_with_variation(
        "SELECT COUNT(*) FROM interactions WHERE email_clicked = 1",
        period
    )

def conversions_kpi(period="weekly"):
    return metric_with_variation(
        "SELECT COUNT(*) FROM interactions WHERE conversion = 1",
        period
    )
