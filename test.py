from rag.retrieval import retrieve_chunks
from llm.ollama_client import generate
from rag.service import answer_with_rag

def test_retrieval():
    query = "Qu'est-ce que le cycle ingénieur à l'ESILV ?"

    docs = retrieve_chunks(query, k=5)

    print("\n=== QUERY ===")
    print(query)

    print("\n=== RESULTS ===")
    for i, doc in enumerate(docs):
        print(f"\n--- Chunk {i+1} ---")
        print(doc["text"][:500])
        print("Source:", doc["source"])

def test_llm():
    prompt = "Explique ce qu'est l'ESILV en une phrase."

    response = generate(prompt)
    print("=== PROMPT ===")
    print(prompt)
    print("\n=== RESPONSE ===")
    print(response)

def test_all():
    question = "Quelles sont les modalités d'admission à l'ESILV ?"

    response = answer_with_rag(question)

    print("\n=== QUESTION ===")
    print(question)

    print("\n=== ANSWER ===")
    print(response["answer"])
    print("\n=== SOURCES ===")
    for s in response["sources"]:
        print("-", s)

if __name__ == "__main__":
    #test_retrieval()
    #test_llm()
    test_all()