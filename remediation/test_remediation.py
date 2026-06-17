from report_loader import (
    load_file_report,
    read_source_file
)

from prompt_builder import (
    build_remediation_prompt
)

from llm_client import remediate_code

from file_utils import save_text
import os


# ----------------------------------
# Load Analysis Report
# ----------------------------------

report = load_file_report(
    "../outputs/file_reports/main_analysis.json"
)

print(
    f"Loaded report for: "
    f"{report['file']}"
)

print(
    f"Violations Found: "
    f"{len(report['violations'])}"
)

# ----------------------------------
# Read Source Code
# ----------------------------------

source_code = read_source_file(
    report["path"]
)

# ----------------------------------
# Build Prompt
# ----------------------------------

prompt = build_remediation_prompt(
    source_code,
    report["violations"],
    report["context"],
    report["retrieved_rules"],
    report["file"]
)

save_text(
    prompt,
    "../outputs/remediation_test/main_prompt.txt"
)

print("Prompt generated.")

# ----------------------------------
# Call GPT
# ----------------------------------

response = remediate_code(
    prompt,
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4.1",
    temperature=0
)

print("GPT remediation completed.")

# ----------------------------------
# Save Remediated File
# ----------------------------------

save_text(
    response,
    "../outputs/remediation_test/main_remediated.c"
)

print(
    "Saved: "
    "outputs/remediation_test/main_remediated.c"
)