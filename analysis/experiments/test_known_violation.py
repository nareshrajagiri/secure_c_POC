from pathlib import Path

from rule_retriever import retrieve_rules
from prompt_builder import build_analysis_prompt
from llm_client import analyze_code

code = Path(
    "test_vulnerable.c"
).read_text()

rules = retrieve_rules(
    code,
    k=15
)

print("\nRetrieved Rules:\n")

for r in rules:
    print(
        r.metadata["rule_id"]
    )

prompt = build_analysis_prompt(
    "test_vulnerable.c",
    code,
    {},
    rules
)

result = analyze_code(
    prompt,
    api_key="",
    model_name="gpt-4.1",
    temperature=0
)

print("\nResult:\n")
print(result)