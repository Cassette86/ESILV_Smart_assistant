"""
Module de retrieval : interroge l'index Chroma (data/index) et renvoie les chunks pertinents.
"""

import chromadb
from chromadb.utils import embedding_functions

INDEX_DIR = "data/index"
COLLECTION_NAME = "esilv_rag"


def _get_embedding_function():
    """
    On utilise l'embedding ONNX MiniLM (celui que Chroma a téléchargé chez toi).
    On garde un fallback "DefaultEmbeddingFunction" si besoin.
    """
    try:
        return embedding_functions.ONNXMiniLM_L6_V2()
    except Exception:
        return embedding_functions.DefaultEmbeddingFunction()


def get_collection():
    client = chromadb.PersistentClient(path=INDEX_DIR)
    emb_fn = _get_embedding_function()

    # Important : fournir la même embedding_function que celle utilisée pour requêter par texte.
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=emb_fn
    )


def retrieve_context(question: str, k: int = 5):
    """
    Retourne une liste de passages (chunks) + leurs métadonnées.
    """
    col = get_collection()
    res = col.query(
        query_texts=[question],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    docs = res["documents"][0]
    metas = res["metadatas"][0]
    dists = res["distances"][0]

    contexts = []
    for doc, meta, dist in zip(docs, metas, dists):
        contexts.append({
            "text": doc,
            "source": meta.get("source", "unknown"),
            "distance": dist
        })
    return contexts
