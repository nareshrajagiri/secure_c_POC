import json
from datetime import datetime

from .prompt_builder import build_remediation_prompt
from .llm_client import remediate_code
from .report_loader import (
    get_analysis_reports,
    load_file_report,
    read_source_file
)
from .file_utils import save_text


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
        # Save Prompt
        # ----------------------------------------------

        save_text(
            prompt,
            f"outputs/prompts/{report['file']}.txt"
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
        # Save Raw LLM Response
        # ----------------------------------------------

        save_text(
            response,
            f"outputs/raw_llm_responses/{report['file']}.txt"
        )

        # ----------------------------------------------
        # Save Remediated Source Code
        # ----------------------------------------------

        save_text(
            response,
            f"outputs/remediated_code/{report['file']}"
        )

        # ----------------------------------------------
        # Create Remediation Report
        # ----------------------------------------------

        remediation_report = {
            "file": report["file"],
            "original_violations": len(
                report["violations"]
            ),
            "rules": report["retrieved_rules"],
            "status": "remediated",
            "timestamp": datetime.now().isoformat(),
            "output_file":
                f"outputs/remediated_code/{report['file']}"
        }

        # ----------------------------------------------
        # Save Remediation Report
        # ----------------------------------------------

        save_text(
            json.dumps(
                remediation_report,
                indent=4
            ),
            (
                f"outputs/remediation_reports/"
                f"{report['file']}_remediation.json"
            )
        )

        processed_count += 1

        print("Remediation Completed")
        print(
            f"Output saved to "
            f"outputs/remediated_code/{report['file']}"
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