"""
ETAPE 2 - CONSTRUCTION DE L'INDEX VECTORIEL (CHROMADB)
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

import os
import json
import chromadb

CHUNKS_FILE = "data/chunks.jsonl"
INDEX_DIR = "data/index"
COLLECTION_NAME = "esilv_rag"


def load_chunks():
    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def main():
    os.makedirs(INDEX_DIR, exist_ok=True)

    client = chromadb.PersistentClient(path=INDEX_DIR)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    chunks = load_chunks()

    ids = []
    documents = []
    metadatas = []

    for i, c in enumerate(chunks):
        ids.append(f"chunk_{i}")
        documents.append(c["chunk"])
        metadatas.append({"source": c["source"]})

    print(f"[INFO] Adding {len(chunks)} chunks to Chroma collection '{COLLECTION_NAME}'...")
    collection.add(ids=ids, documents=documents, metadatas=metadatas)

    print("[OK] Index built successfully!")
    print(f"[OK] Saved in: {INDEX_DIR}")


if __name__ == "__main__":
    main()
