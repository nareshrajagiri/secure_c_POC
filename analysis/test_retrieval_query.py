from pathlib import Path
from rule_retriever import vector_store

code = Path(
    "../HVAC_Project/Core/Src/main.c"
).read_text(
    encoding="utf-8",
    errors="ignore"
)

query = """
STM32 UART ADC TIM GPIO
error handling
return value checking
global variables
shared state
interrupt safety
"""

print("\nFULL FILE RETRIEVAL\n")

results = vector_store.similarity_search(
    code,
    k=15
)

for doc in results:
    print(doc.metadata["rule_id"])

print("\nCONTEXT QUERY RETRIEVAL\n")

results = vector_store.similarity_search(
    query,
    k=15
)

for doc in results:
    print(doc.metadata["rule_id"])



"""output
(venv) PS C:\Users\nares\OneDrive\Desktop\Secure_C_POC\analysis> python test_retrieval_query.py

FULL FILE RETRIEVAL

CON33-C
MSC40-C
ERR33-C
DCL40-C
DCL31-C
MSC32-C
MSC38-C
ARR30-C
SIG31-C
EXP33-C
MSC30-C
CON32-C
PRE32-C
ARR38-C
CON37-C

CONTEXT QUERY RETRIEVAL

ERR33-C
CON33-C
MSC40-C
SIG31-C
ARR38-C
DCL40-C
CON32-C
FIO45-C
SIG30-C
ARR30-C
MSC32-C
FIO47-C
INT30-C
DCL31-C
CON37-C
(venv) PS C:\Users\nares\OneDrive\Desktop\Secure_C_POC\analysis> 
"""