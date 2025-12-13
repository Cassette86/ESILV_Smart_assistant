"""
Service RAG : (1) retrieval -> (2) construction du prompt -> (3) génération LLM -> (4) retour réponse + sources
"""
'''
from rag.retrieval import retrieve_context
from llm.ollama_client import generate


def build_prompt(question: str, contexts: list) -> str:
    """
    Construit un prompt "grounded" : le modèle doit répondre UNIQUEMENT à partir du contexte.
    """
    context_block = "\n\n".join(
        [f"[Source: {c['source']}]\n{c['text']}" for c in contexts]
    )

    prompt = f"""
Tu es un assistant dédié à l'ESILV.
Réponds en français, de façon claire et structurée.
Tu DOIS utiliser uniquement le CONTEXTE fourni.
Si l'information n'est pas dans le contexte, dis : "Je n'ai pas l'information dans les documents fournis."

CONTEXTE :
{context_block}

QUESTION :
{question}

RÉPONSE :
""".strip()

    return prompt


def answer_with_rag(question: str, k: int = 5) -> dict:
    contexts = retrieve_context(question, k=k)
    prompt = build_prompt(question, contexts)
    answer = generate(prompt)

    # sources uniques (sans doublons)
    sources = []
    seen = set()
    for c in contexts:
        s = c["source"]
        if s not in seen:
            sources.append(s)
            seen.add(s)

    return {
        "answer": answer                            ,
        "sources": sources,                                         
        "contexts": contexts
    }


'''