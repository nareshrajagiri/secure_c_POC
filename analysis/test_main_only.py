import json
from pathlib import Path

from .rule_retriever import retrieve_rules
from .prompt_builder import build_analysis_prompt
from .llm_client import analyze_code

from .analysis_node import (
    read_source_file,
    get_file_context
)

# -----------------------------------
# CONFIG
# -----------------------------------

PROJECT_PATH = r"HVAC_Project"

CONTEXT_PATH = "context.json"

API_KEY = ""
TEMPERATURE = 0

MAIN_FILE = (
    Path(PROJECT_PATH)
    / "Core"
    / "Src"
    / "main.c"
)

# -----------------------------------
# OUTPUT DIR
# -----------------------------------

OUTPUT_DIR = Path(
    "outputs/main_debug"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# -----------------------------------
# READ SOURCE
# -----------------------------------

print("\nReading main.c")
print("Current Working Directory:")
print(Path.cwd())

print("\nTrying to read:")
print(MAIN_FILE.resolve())

main_code = read_source_file(
    str(MAIN_FILE)
)

print(
    f"Source Length: "
    f"{len(main_code)} characters"
)

# -----------------------------------
# RETRIEVE RULES
# -----------------------------------

print("\nRetrieving Rules")

retrieved_rules = retrieve_rules(
    main_code,
    k=15
)

rules_output = []

for doc in retrieved_rules:

    rules_output.append(
        {
            "metadata":
            doc.metadata,

            "content":
            doc.page_content
        }
    )

with open(
    OUTPUT_DIR /
    "retrieved_rules.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        rules_output,
        f,
        indent=4
    )

# -----------------------------------
# CONTEXT
# -----------------------------------

print("\nLoading Context")

file_context = get_file_context(
    "main.c",
    CONTEXT_PATH
)

# -----------------------------------
# PROMPT
# -----------------------------------

print("\nBuilding Prompt")

prompt = build_analysis_prompt(
    "main.c",
    main_code,
    file_context,
    retrieved_rules
)

with open(
    OUTPUT_DIR /
    "prompt.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(prompt)

# -----------------------------------
# GPT-4.1 MINI
# -----------------------------------

print("\nRunning GPT-4.1-mini")

response_mini = analyze_code(
    prompt,
    API_KEY,
    "gpt-4.1-mini",
    TEMPERATURE
)

with open(
    OUTPUT_DIR /
    "raw_response_mini.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(response_mini)

# -----------------------------------
# GPT-4.1 FULL
# -----------------------------------

print("\nRunning GPT-4.1")

response_full = analyze_code(
    prompt,
    API_KEY,
    "gpt-4.1",
    TEMPERATURE
)

with open(
    OUTPUT_DIR /
    "raw_response_full.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(response_full)

# -----------------------------------
# DONE
# -----------------------------------

print("\nCompleted")

print(
    "\nGenerated Files:"
)

print(
    "outputs/main_debug/retrieved_rules.json"
)

print(
    "outputs/main_debug/prompt.txt"
)

print(
    "outputs/main_debug/raw_response_mini.txt"
)

print(
    "outputs/main_debug/raw_response_full.txt"
)