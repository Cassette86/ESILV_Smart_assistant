def detect_theme(query: str) -> str:
    query = query.lower()

    if "admission" in query or "candidature" in query or "inscription" in query:
        return "Admissions"
    if "alternance" in query:
        return "Alternance"
    if "formation" in query or "programme" in query or "majeure" in query:
        return "Formations"
    if "international" in query:
        return "International"

    return "Other"