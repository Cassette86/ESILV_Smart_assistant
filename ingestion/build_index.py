"""
ETAPE 3 - CONSTRUCTION DE L'INDEX VECTORIEL (CHROMADB)
------------------------------------------------------

Objectif :
- Lire le fichier data/chunks.jsonl (produit à l'étape 1).
- Stocker chaque chunk dans une base vectorielle persistante (ChromaDB).
- Associer des métadonnées (source du document) à chaque chunk.
- Préparer le système RAG : le chatbot pourra ensuite retrouver les passages
  pertinents via une recherche sémantique.

Résultat :
- Création d'un dossier data/index/ contenant l'index Chroma persistant.
"""

import chromadb
from chromadb.utils import embedding_functions
import json

CHROMA_DIR = "data/chroma"
COLLECTION_NAME = "esilv_docs"

def build_or_update_index(chunks):
    BATCH_SIZE = 1000
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    total = len(chunks)
    print(f"Indexing {total} chunks in batches...")

    for i in range(0, total, BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]

        ids = [chunk["id"] for chunk in batch]
        texts = [chunk["text"] for chunk in batch]
        metadatas = [{"source": chunk["source"]} for chunk in batch]

        collection.upsert(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

        print(f"✓ Indexed {i + len(batch)} / {total}")

    print("✅ Indexation Chroma terminée")

def load_chunks(jsonl_path):
    chunks = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            obj = json.loads(line)
            chunks.append({
                "id": f"chunk_{i}",
                "text": obj["chunk"],
                "source": obj["source"]
            })
    return chunks

if __name__ == "__main__":
    DIR_CHUNKS = "data/chunks.jsonl"

    chunks = load_chunks(DIR_CHUNKS)
    build_or_update_index(chunks)

    print(f"Indexing {len(chunks)} chunks")
    print(chunks[0]["text"][:200])
    print(chunks[0]["source"])