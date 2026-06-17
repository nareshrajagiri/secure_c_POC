from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

print("Loading Vector Store...")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = FAISS.load_local(
    "vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)

print("Vector Store Loaded")

#query = "buffer overflow due to strcpy"
#query = "memory leak because malloc memory not freed"
#query = "integer overflow during arithmetic"
query = "null pointer dereference"

print(f"\nQuery: {query}")

results = vector_store.similarity_search(
    query,
    k=5
)

print("\nTop Matches:\n")

for i, doc in enumerate(results, start=1):

    print("=" * 60)

    print(f"Result #{i}")

    print(doc.metadata)

    print()

    print(doc.page_content[:500])

    print()

    