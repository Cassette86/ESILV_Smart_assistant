"""
Answer Agent
Responsabilité unique :
- Générer une réponse à partir d'une question
- Avec ou sans contexte
"""

from llm.ollama_client import generate


# ========================= PROMPTS =========================

def build_rag_prompt(question: str, contexts: list[dict]) -> str:
    """
    Prompt RAG strictement grounded
    """

    context_block = "\n\n".join(
        [f"[Source: {c['source']}]\n{c['text']}" for c in contexts]
    )

    prompt = f"""
Tu es un assistant officiel de l'ESILV.

Règles IMPORTANTES :
- Tu dois répondre uniquement à partir du CONTEXTE ci-dessous.
- Tu réponds en français.
- Tu es clair, structuré et concis.
- Si l'information n'est pas présente dans le contexte, dis exactement :
  "Je n'ai pas l'information dans les documents fournis."

CONTEXTE :
{context_block}

QUESTION :
{question}

RÉPONSE :
""".strip()

    return prompt


def build_clarification_prompt(question: str) -> str:
    """
    Prompt pour questions vagues ou incomplètes
    """

    prompt = f"""
Tu es un assistant officiel de l'ESILV.

La question de l'utilisateur est trop vague ou imprécise.
Demande poliment une clarification en français,
sans inventer d'information.

QUESTION :
{question}

RÉPONSE :
""".strip()

    return prompt


# ========================= ANSWER AGENT =========================

def answer_with_context(question: str, contexts: list[dict]) -> str:
    """
    Génère une réponse à partir du contexte (RAG)
    """
    prompt = build_rag_prompt(question, contexts)
    return generate(prompt)


def answer_without_context(question: str) -> str:
    """
    Génère une réponse sans contexte (clarification)
    """
    prompt = build_clarification_prompt(question)
    return generate(prompt)
