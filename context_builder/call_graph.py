import os
import re

from .symbol_ownership import build_symbol_ownership


def extract_function_bodies(content, known_functions):
    """
    Extract complete function bodies using brace tracking.
    Returns:
    {
        "function_name": "body text"
    }
    """

    function_bodies = {}

    lines = content.splitlines()

    current_function = None
    collecting = False
    brace_depth = 0
    body_lines = []

    for line in lines:

        stripped = line.strip()

        # Detect function definition line
        if not collecting:

            for func in known_functions:

                if re.search(rf"\b{func}\s*\(", stripped):

                    current_function = func
                    collecting = True
                    body_lines = [line]

                    brace_depth += line.count("{")
                    brace_depth -= line.count("}")

                    break

            continue

        # Collect function body
        body_lines.append(line)

        brace_depth += line.count("{")
        brace_depth -= line.count("}")

        # Function completed
        if collecting and brace_depth == 0 and "{" in "".join(body_lines):

            function_bodies[current_function] = "\n".join(
                body_lines
            )

            current_function = None
            collecting = False
            body_lines = []

    return function_bodies


def build_call_graph(application_files):

    ownership = build_symbol_ownership(
        application_files
    )

    known_functions = set(
        ownership["functions"].keys()
    )

    call_graph = {}

    for filepath in application_files:

        if not filepath.endswith(".c"):
            continue

        try:

            with open(
                filepath,
                "r",
                errors="ignore"
            ) as f:

                content = f.read()

            function_bodies = extract_function_bodies(
                content,
                known_functions
            )

            for current_function, body in function_bodies.items():

                call_graph[current_function] = []

                for called_function in known_functions:

                    if called_function == current_function:
                        continue

                    pattern = rf"\b{called_function}\s*\("

                    if re.search(pattern, body):

                        call_graph[current_function].append(
                            called_function
                        )

        except Exception as e:

            print(
                f"Failed: {filepath}"
            )

    return call_graph


if __name__ == "__main__":

    from context_builder import (
        discover_application_files
    )

    project_path = "../HVAC_Project"

    files = discover_application_files(
        project_path
    )

    graph = build_call_graph(
        files
    )

    from pprint import pprint

    pprint(graph)
