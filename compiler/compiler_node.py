import json
from pathlib import Path

from compiler.build_executor import run_build
from compiler.log_parser import parse_build_log


def run_compiler(build_project_path: str):
    """
    Run STM32 compilation and generate compiler report.
    """

    print("=" * 60)
    print("Starting Compiler Node...")
    print("=" * 60)

    build_result = run_build(build_project_path)

    parse_result = parse_build_log(
        build_result["build_log"]
    )

    report = {
        "build_project_path": build_project_path,

        "status": parse_result["status"],
        "build_success": build_result["success"],
        "return_code": build_result["return_code"],

        "error_count": parse_result["error_count"],
        "warning_count": parse_result["warning_count"],

        "errors": parse_result["errors"],
        "warnings": parse_result["warnings"],

        "build_log": build_result["build_log"]
    }

    output_dir = Path("compiler/outputs")
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path = output_dir / "compiler_report.json"

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            report,
            f,
            indent=4
        )

    print()
    print(f"Compiler Report Saved : {report_path}")

    return report