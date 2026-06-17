import os
import re


def extract_global_variables(content):
    """
    Extract only true global variables.
    Ignore variables declared inside functions.
    """

    globals_found = []

    lines = content.splitlines()

    brace_depth = 0

    global_pattern = re.compile(
        r'^\s*(?:static\s+)?'
        r'(?:uint\d+_t|int\d+_t|char|int|float|double|bool)\s+'
        r'([A-Za-z_]\w*)\s*(?:=.*?)?;'
    )

    for line in lines:

        stripped = line.strip()

        # Only inspect declarations outside functions
        if brace_depth == 0:

            match = global_pattern.match(stripped)

            if match:

                globals_found.append(
                    match.group(1)
                )

        brace_depth += line.count("{")
        brace_depth -= line.count("}")

    return globals_found


def build_symbol_ownership(application_files):

    ownership = {
        "functions": {},
        "globals": {}
    }

    function_pattern = re.compile(
        r'^\s*(?:void|int|char|float|double|uint\d+_t|int\d+_t|bool)\s+([A-Za-z_]\w*)\s*\(',
        re.MULTILINE
    )

    for filepath in application_files:

        if not filepath.endswith(".c"):
            continue

        filename = os.path.basename(filepath)

        try:

            with open(
                filepath,
                "r",
                errors="ignore"
            ) as f:

                content = f.read()

            # ----------------------------------
            # Function Ownership
            # ----------------------------------

            functions = function_pattern.findall(
                content
            )

            for func in functions:

                ownership["functions"][func] = filename

            # ----------------------------------
            # Global Ownership
            # ----------------------------------

            globals_found = extract_global_variables(
                content
            )

            for var in globals_found:

                ownership["globals"][var] = filename

        except Exception as e:

            print(
                f"Failed: {filepath}"
            )

    return ownership


# ----------------------------------
# Testing
# ----------------------------------

if __name__ == "__main__":

    from context_builder import (
        discover_application_files
    )

    files = discover_application_files(
        "../HVAC_Project"
    )

    ownership = build_symbol_ownership(
        files
    )

    from pprint import pprint

    pprint(ownership)
