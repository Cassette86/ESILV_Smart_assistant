def detect_intent(user_input: str) -> str:
    text = user_input.lower()

    if any(k in text for k in [
        "recontact", "contact", "inscription", "être appelé", "rappel"
    ]):
        return "contact"

    if any(k in text for k in [
        "?", "comment", "quand", "où", "quel", "quelle"
    ]):
        return "rag"

    return "clarification"


def orchestrate(user_input: str, state: dict) -> dict:
    intent = detect_intent(user_input)

    if intent == "contact":
        return {
            "intent": "contact",
            "action": "switch_to_contact"
        }

    if intent == "rag":
        return {
            "intent": "rag",
            "action": "answer_with_rag"
        }

    return {
        "intent": "clarification",
        "action": "ask_clarification",
        "message": "Pouvez-vous préciser votre question afin que je puisse mieux vous répondre ?"
    }
