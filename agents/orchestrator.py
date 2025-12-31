from agents.retrieval_agent import retrieve_context
from agents.answer_agent import (
    answer_with_context,
    answer_without_context
)

# ========================= INTENT DETECTION =========================

def detect_intent(user_input: str) -> str:
    text = user_input.lower()

    if any(k in text for k in [
        "recontact", "contact", "inscription", "être appelé", "rappel"
    ]):
        return "contact"

    if any(k in text for k in [
        "?", "comment", "quand", "où", "quel", "quelle",
        "décris", "explique", "présente", "c'est quoi", "qui est",
        "donne moi", "fournis", "informations", "détails",
        "modalités", "procédure"
    ]):
        return "rag"

    return "clarification"


# ========================= ORCHESTRATOR AGENT =========================

def orchestrate(user_input: str, state: dict) -> dict:
    intent = detect_intent(user_input)

    # ---------- CONTACT ----------
    if intent == "contact":
        return {
            "intent": "contact",
            "action": "switch_to_contact"
        }

    # ---------- RAG ----------
    if intent == "rag":
        retrieval = retrieve_context(user_input)

        answer = answer_with_context(
            question=user_input,
            contexts=retrieval["contexts"]
        )

        return {
            "intent": "rag",
            "action": "answer",
            "answer": answer,
            "rag_results": {
                "sources": retrieval["sources"],
                "similarities": retrieval["similarities"]
            }
        }

    # ---------- CLARIFICATION ----------
    answer = answer_without_context(user_input)

    return {
        "intent": "clarification",
        "action": "answer",
        "answer": answer,
        "rag_results": {
            "sources": [],
            "similarities": []
        }
    }
