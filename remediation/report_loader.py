from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_analysis_reports():

    reports_dir = (
        PROJECT_ROOT /
        "analysis" /
        "outputs" /
        "file_reports"
    )

    return list(reports_dir.glob("*.json"))


def load_file_report(report_path):

    with open(report_path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_source_path(relative_path):

    relative_path = (
        relative_path
        .replace("\\", "/")
        .replace("../", "")
    )

    return PROJECT_ROOT / relative_path


def read_source_file(relative_path):

    source_path = resolve_source_path(relative_path)

    with open(source_path, "r", encoding="utf-8") as f:
        return f.read()