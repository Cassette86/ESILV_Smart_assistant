from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

# ===== chemins =====
BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "data" / "chroma"
COLLECTION_NAME = "esilv_docs"

# ===== embedding model (DOIT matcher l’indexation) =====
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ===== init Chroma client & collection =====
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn
)


def retrieve_chunks(question: str, k: int = 5):
    """
    Retrieval ChromaDB pour le RAG
    """
    results = collection.query(
        query_texts=[question],
        n_results=k
    )

    contexts = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for text, meta, dist in zip(documents, metadatas, distances):
        contexts.append({
            "text": text,
            "source": meta.get("source", "unknown"),
            "distance": float(dist)
        })

    return contexts
