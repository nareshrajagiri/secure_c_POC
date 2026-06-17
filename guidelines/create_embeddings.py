import json
import os

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# --------------------------
# Load Secure-C Rules
# --------------------------

with open(
    "secure_c_rules_final.json",
    "r",
    encoding="utf-8"
) as f:
    rules = json.load(f)

documents = []

for rule in rules:

    content = f"""
Rule ID: {rule['rule_id']}

Category: {rule['category']}

Description:
{rule['description']}

Fix:
{rule['fix']}
"""

    doc = Document(
        page_content=content,
        metadata={
            "rule_id": rule["rule_id"],
            "category": rule["category"]
        }
    )

    documents.append(doc)

print(f"Documents Created: {len(documents)}")

# --------------------------
# Create Embeddings
# --------------------------

print("Creating OpenAI Embeddings...")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# --------------------------
# Create FAISS Index
# --------------------------

print("Building FAISS Index...")

vector_store = FAISS.from_documents(
    documents,
    embeddings
)

# --------------------------
# Save Vector Store
# --------------------------

save_path = "vector_store"

vector_store.save_local(save_path)

print("FAISS Index Saved Successfully!")
print(f"Location: {save_path}")