from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

if __name__ == "__main__":
    """
    Debug ChromaDB : vérifier le nombre de documents indexés
    """

    BASE_DIR = Path(__file__).resolve().parent
    CHROMA_DIR = BASE_DIR / "data" / "chroma"

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )
    collection = client.get_or_create_collection(
        name="esilv_docs",
        embedding_function=embedding_fn
    )

    print("COUNT =", collection.count())