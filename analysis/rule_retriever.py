from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_STORE_PATH = (
    BASE_DIR
    / "guidelines"
    / "vector_store"
)


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = FAISS.load_local(
    str(VECTOR_STORE_PATH),
    embeddings,
    allow_dangerous_deserialization=True
)


def retrieve_rules(code_text, k=15):

    results = vector_store.similarity_search(
        code_text,
        k=k
    )

    return results