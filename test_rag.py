'''
from rag.service import answer_with_rag

if __name__ == "__main__":
    while True:
        q = input("\nQuestion (ou 'exit'): ").strip()
        if q.lower() == "exit":
            break

        res = answer_with_rag(q, k=5)

        print("\n--- REPONSE ---")
        print(res["answer"])

        print("\n--- SOURCES ---")
        for s in res["sources"]:
            print("-", s)

'''
