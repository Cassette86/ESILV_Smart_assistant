from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

# ======================= CONFIGURATION =======================
BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "data" / "chroma"
COLLECTION_NAME = "esilv_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ======================= INIT CHROMA =======================
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

# ======================= RETRIEVAL AGENT =======================
def retrieve_context(query: str, k: int = 5) -> dict:
    """
    Retrieval Agent
    - Interroge ChromaDB
    - Retourne contexte + sources + similarités
    """

    results = collection.query(
        query_texts=[query],
        n_results=k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    contexts = []
    sources = []
    similarities = []

    for text, meta, dist in zip(documents, metadatas, distances):
        source = meta.get("source", "unknown")

        contexts.append({
            "text": text,
            "source": source
        })

        sources.append(source)
        similarities.append(float(dist))

    # suppression doublons sources (ordre conservé)
    unique_sources = list(dict.fromkeys(sources))

    return {
        "documents": [c["text"] for c in contexts],
        "contexts": contexts,
        "sources": unique_sources,
        "similarities": similarities
    }