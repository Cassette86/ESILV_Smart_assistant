from analytics.db import get_db

# =========================================================
# Helpers – filtres temporels
# =========================================================

def _period_filter(period: str):
    if period == "weekly":
        return "timestamp >= date('now', '-7 days')"
    if period == "monthly":
        return "timestamp >= date('now', '-30 days')"
    if period == "quarterly":
        return "timestamp >= date('now', '-90 days')"
    if period == "yearly":
        return "timestamp >= date('now', '-365 days')"
    return "1=1"


def _previous_period(period: str):
    if period == "weekly":
        return "timestamp BETWEEN date('now', '-14 days') AND date('now', '-7 days')"
    if period == "monthly":
        return "timestamp BETWEEN date('now', '-60 days') AND date('now', '-30 days')"
    if period == "quarterly":
        return "timestamp BETWEEN date('now', '-180 days') AND date('now', '-90 days')"
    if period == "yearly":
        return "timestamp BETWEEN date('now', '-730 days') AND date('now', '-365 days')"
    return "1=1"


# =========================================================
# KPI COUNTERS (sans variation)
# =========================================================

def users_count(period):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(DISTINCT user_id)
        FROM interactions
        WHERE {_period_filter(period)}
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
        WHERE {_period_filter(period)}
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
        WHERE {_period_filter(period)}
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
        WHERE {_period_filter(period)}
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
        WHERE {_period_filter(period)}
        AND conversion = 1
    """)
    value = cur.fetchone()[0]
    conn.close()
    return value


# =========================================================
# QUERIES BY THEME
# =========================================================

def queries_by_theme(period):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT theme, COUNT(*) AS count
        FROM interactions
        WHERE {_period_filter(period)}
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
        SELECT {group_by} AS time_unit, COUNT(*)
        FROM interactions
        WHERE {_period_filter(period)}
        GROUP BY time_unit
        ORDER BY time_unit
    """)

    rows = cur.fetchall()
    conn.close()
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
        WHERE {_period_filter(period)}
    """)
    value = cur.fetchone()[0]
    conn.close()
    return round(value, 3) if value else 0.0


def top_used_documents(period, limit=5):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT used_sources, COUNT(*) AS count
        FROM interactions
        WHERE {_period_filter(period)}
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
        SELECT used_sources, COUNT(*) AS count
        FROM interactions
        WHERE {_period_filter(period)}
        GROUP BY used_sources
        ORDER BY count ASC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]


# =========================================================
# KPI AVEC VARIATION (Δ) – VERSION ROBUSTE
# =========================================================

def metric_with_variation(
    base_query: str,
    period="weekly",
    extra_condition: str | None = None
):
    conn = get_db()
    cur = conn.cursor()

    # ----- période actuelle
    conditions_now = [_period_filter(period)]
    if extra_condition:
        conditions_now.append(extra_condition)

    where_now = " AND ".join(conditions_now)

    cur.execute(f"""
        {base_query}
        WHERE {where_now}
    """)
    current = cur.fetchone()[0] or 0

    # ----- période précédente
    conditions_prev = [_previous_period(period)]
    if extra_condition:
        conditions_prev.append(extra_condition)

    where_prev = " AND ".join(conditions_prev)

    cur.execute(f"""
        {base_query}
        WHERE {where_prev}
    """)
    previous = cur.fetchone()[0] or 0

    conn.close()

    if previous == 0:
        variation = None
    else:
        variation = round(((current - previous) / previous) * 100, 1)

    return current, variation


# =========================================================
# KPI AVEC VARIATION – APPELS
# =========================================================

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
        "SELECT COUNT(*) FROM interactions",
        period,
        extra_condition="email_clicked = 1"
    )


def conversions_kpi(period="weekly"):
    return metric_with_variation(
        "SELECT COUNT(*) FROM interactions",
        period,
        extra_condition="conversion = 1"
    )
