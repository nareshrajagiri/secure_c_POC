import json
from pathlib import Path

from rule_retriever import retrieve_rules
from prompt_builder import build_analysis_prompt
from llm_client import analyze_code

code = Path(
    "../HVAC_Project/Core/Src/main.c"
).read_text(
    encoding="utf-8",
    errors="ignore"
)

dummy_context = {
    "owned_functions": [],
    "called_functions": [],
    "peripherals": [],
    "shared_states": [],
    "protected_regions": []
}

for k in [5, 15]:

    print(f"\n{'='*60}")
    print(f"TESTING K = {k}")
    print(f"{'='*60}")

    rules = retrieve_rules(
        code,
        k=k
    )

    prompt = build_analysis_prompt(
        "main.c",
        code,
        dummy_context,
        rules
    )

    result = analyze_code(
        prompt,
        api_key="",
        model_name="gpt-4.1-mini",
        temperature=0
    )

    print(result)