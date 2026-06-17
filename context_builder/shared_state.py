import os
import re

from .symbol_ownership import build_symbol_ownership


def build_shared_state_map(application_files):

    ownership = build_symbol_ownership(
        application_files
    )

    globals_map = ownership["globals"]

    shared_state = {}

    for variable, owner_file in globals_map.items():

        used_by = []

        pattern = re.compile(
            rf"\b{re.escape(variable)}\b"
        )

        for filepath in application_files:

            if not filepath.endswith(".c"):
                continue

            filename = os.path.basename(filepath)

            if filename == owner_file:
                continue

            try:

                with open(
                    filepath,
                    "r",
                    errors="ignore"
                ) as f:

                    content = f.read()

                if pattern.search(content):

                    used_by.append(filename)

            except Exception:

                pass

        if used_by:

            shared_state[variable] = {
                "defined_in": owner_file,
                "used_by": used_by
            }

    return shared_state


if __name__ == "__main__":

    from context_builder import (
        discover_application_files
    )

    files = discover_application_files(
        "../HVAC_Project"
    )

    state_map = build_shared_state_map(
        files
    )

    from pprint import pprint

    pprint(state_map)
