from pathlib import Path
import json

from rule_retriever import retrieve_rules
from prompt_builder import build_analysis_prompt
from llm_client import analyze_code

code = Path(
    "test_10_violations.c"
).read_text(
    encoding="utf-8"
)

rules = retrieve_rules(
    code,
    k=20
)

prompt = build_analysis_prompt(
    "test_10_violations.c",
    code,
    {},
    rules
)

import os

result = analyze_code(
    prompt=prompt,
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4.1",
    temperature=0
)
Path("outputs").mkdir(
    exist_ok=True
)

with open(
    "outputs/test_10_rule_validation.json",
    "w",
    encoding="utf-8"
) as f:

    f.write(result)

print(
    "\nValidation Report Generated:\n"
)

print(
    "outputs/test_10_rule_validation.json"
)