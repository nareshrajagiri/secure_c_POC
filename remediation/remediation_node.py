
from .prompt_builder import build_remediation_prompt
from .llm_client import remediate_code
from .report_loader import (
    get_analysis_reports,
    load_file_report,
    read_source_file
)
from .file_utils import save_text
from pathlib import Path
import json


def run_remediation(
    api_key,
    model_name,
    temperature,
    status_callback=None
):
    def update(message):
        if status_callback:
            status_callback(message)

        print(message)

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
    REPORT_DIR = (
        Path(__file__).resolve().parent.parent
        / "outputs"
        / "remediation_reports"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )
    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------
    # Process Each Report
    # --------------------------------------------------

    for report_file in report_files:

        report = load_file_report(report_file)

        update(
            f"🔧 Processing {report['file']}"
        )

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

        # ----------------------------------------------
        # Create Remediation Report
        # ----------------------------------------------

        remediation_report = {
            "file": report["file"],
            "violations_fixed": len(
                report["violations"]
            ),
            "rules": list(
                {
                    violation["rule_id"]
                    for violation in report["violations"]
                }
            ),
            "status": "remediated"
        }
        # ----------------------------------------------
        # Save Remediation Report
        # ----------------------------------------------

        save_text(
            json.dumps(
                remediation_report,
                indent=4
            ),
            str(
                REPORT_DIR /
                f"{report['file']}_remediation.json"
            )
        )

        processed_count += 1

        update(
            "✓ Remediation Complete"
        )
        update(
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

    remediation_summary = {
        "reports_found": len(report_files),
        "files_remediated": processed_count,
        "files_skipped": skipped_count
    }

    save_text(
        json.dumps(
            remediation_summary,
            indent=4
        ),
        str(
            Path(__file__).resolve().parent.parent
            / "outputs"
            / "remediation_summary.json"
        )
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

