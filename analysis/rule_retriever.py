from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_STORE_PATH = (
    BASE_DIR
    / "guidelines"
    / "vector_store"
)


def get_vector_store(api_key):

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key
    )

    return FAISS.load_local(
        str(VECTOR_STORE_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve_rules(
    code,
    api_key
):

    vector_store = get_vector_store(
        api_key
    )

    return vector_store.similarity_search(
        code,
        k=10
    )