from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

from core.documents import build_problem_documents


BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_DIR = BASE_DIR / "data" / "processed" / "faiss_index"

EMBED_MODEL = "nomic-embed-text-v2-moe"


def get_embeddings():
    return OllamaEmbeddings(model=EMBED_MODEL)


def build_vector_store():
    docs = build_problem_documents()
    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(docs, embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(INDEX_DIR))

    return vector_store


def load_vector_store():
    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        str(INDEX_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store