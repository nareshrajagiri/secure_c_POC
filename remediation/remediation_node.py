
from .prompt_builder import build_remediation_prompt
from .llm_client import remediate_code
from .report_loader import (
    get_analysis_reports,
    load_file_report,
    read_source_file
)
from .file_utils import save_text
from pathlib import Path


def run_remediation(
    api_key,
    model_name,
    temperature
):

    # --------------------------------------------------
    # Get All Analysis Reports
    # --------------------------------------------------

    report_files = get_analysis_reports()

    print(f"\nFound {len(report_files)} analysis reports.\n")
    processed_count = 0
    skipped_count = 0

    OUTPUT_DIR = (
        Path(__file__).resolve().parent.parent
        / "outputs"
        / "remediated_files"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------
    # Process Each Report
    # --------------------------------------------------

    for report_file in report_files:

        report = load_file_report(report_file)

        print(f"\nProcessing: {report['file']}")

        # ----------------------------------------------
        # Skip Files With No Violations
        # ----------------------------------------------

        if not report["violations"]:
            skipped_count += 1
            print("No violations found. Skipping.")
            continue

        print(
            f"Violations Found: "
            f"{len(report['violations'])}"
        )

        # ----------------------------------------------
        # Read Original Source Code
        # ----------------------------------------------

        source_code = read_source_file(
            report["path"]
        )

        # ----------------------------------------------
        # Build Prompt
        # ----------------------------------------------

        prompt = build_remediation_prompt(
            source_code,
            report["violations"],
            report["context"],
            report["retrieved_rules"],
            report["file"]
        )

        # ----------------------------------------------
        # Call LLM
        # ----------------------------------------------

        response = remediate_code(
            prompt,
            api_key,
            model_name,
            temperature
        )

        # ----------------------------------------------
        # Save Remediated Source Code
        # ----------------------------------------------

        save_text(
            response,
            str(
                OUTPUT_DIR / report["file"]
            )
        )

        processed_count += 1

        print("Remediation Completed")
        print(
            f"Remediated file saved: "
            f"{report['file']}"
        )

    # --------------------------------------------------
    # Finished
    # --------------------------------------------------
    print("\nRemediation Summary")
    print("-" * 30)

    print(
        f"Reports Found      : "
        f"{len(report_files)}"
    )

    print(
        f"Files Remediated   : "
        f"{processed_count}"
    )

    print(
        f"Files Skipped      : "
        f"{skipped_count}"
    )

    print("\nAll remediation tasks completed.\n")

    return {
    "reports_found": len(report_files),
    "files_remediated": processed_count,
    "files_skipped": skipped_count
}

if __name__ == "__main__":
    print(
        "Run from pipeline_runner.py"
    )

"""(venv) PS C:\Users\nares\OneDrive\Desktop\Secure_C_POC> python test_remediation_pipeline.py

Found 10 analysis reports.


Processing: command_handler.c
Violations Found: 2
Remediation Completed
Remediated file saved: command_handler.c

Processing: command_handler.h
No violations found. Skipping.

Processing: main.c
Violations Found: 5
Remediation Completed
Remediated file saved: main.c

Processing: main.h
No violations found. Skipping.

Processing: motor_controller.c
Violations Found: 2
Remediation Completed
Remediated file saved: motor_controller.c

Processing: motor_controller.h
No violations found. Skipping.

Processing: position_sensing.c
Violations Found: 2
Remediation Completed
Remediated file saved: position_sensing.c

Processing: position_sensing.h
No violations found. Skipping.

Processing: status_indicator.c
Violations Found: 4
Remediation Completed
Remediated file saved: status_indicator.c

Processing: status_indicator.h
No violations found. Skipping.

Remediation Summary
------------------------------
Reports Found      : 10
Files Remediated   : 5
Files Skipped      : 5

All remediation tasks completed.

{'reports_found': 10, 'files_remediated': 5, 'files_skipped': 5}
(venv) PS C:\Users\nares\OneDrive\Desktop\Secure_C_POC> """