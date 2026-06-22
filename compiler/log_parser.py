import re
from pathlib import Path


ERROR_PATTERN = re.compile(
    r"(?P<file>.+\.(?:c|h)):(?P<line>\d+):\d+:\s+(?:error|fatal error):\s+(?P<message>.+)"
)
WARNING_PATTERN = re.compile(
    r"(?P<file>.+\.(?:c|h)):(?P<line>\d+):\d+:\s+warning:\s+(?P<message>.+)"
)


def parse_build_log(log_file_path: str):
    """
    Parse GCC build errors from build.log.
    """

    log_text = Path(log_file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    )

    errors = []
    warnings = []

    for match in ERROR_PATTERN.finditer(log_text):

        file_path = match.group("file")
        line_number = int(match.group("line"))
        message = match.group("message").strip()

        errors.append(
            {
                "file": Path(file_path).name,
                "line": line_number,
                "message": message
            }
        )
    for match in WARNING_PATTERN.finditer(log_text):

        file_path = match.group("file")
        line_number = int(match.group("line"))
        message = match.group("message").strip()

        warnings.append(
            {
                "file": Path(file_path).name,
                "line": line_number,
                "message": message
            }
        )

    return {
        "status": "success" if len(errors) == 0 else "failed",

        "error_count": len(errors),
        "warning_count": len(warnings),

        "errors": errors,
        "warnings": warnings
    }