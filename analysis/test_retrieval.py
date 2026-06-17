from pathlib import Path
from rule_retriever import retrieve_rules

code = Path(
    "../HVAC_Project/Core/Src/main.c"
).read_text(
    encoding="utf-8",
    errors="ignore"
)

for k in [5, 10, 15, 20]:

    print(f"\nTOP K = {k}")

    results = retrieve_rules(
        code,
        k=k
    )

    for doc in results:

        print(
            doc.metadata["rule_id"]
        )