import os
import re


def build_interface_contracts(application_files):

    contracts = {}

    prototype_pattern = re.compile(
        r'^\s*([A-Za-z_][\w\s\*]*?)\s+'
        r'([A-Za-z_]\w*)\s*'
        r'\(([^)]*)\)\s*;',
        re.MULTILINE
    )

    for filepath in application_files:

        if not filepath.endswith(".h"):
            continue

        filename = os.path.basename(filepath)

        try:

            with open(
                filepath,
                "r",
                errors="ignore"
            ) as f:

                content = f.read()

            matches = prototype_pattern.findall(
                content
            )

            for return_type, func_name, params in matches:

                contracts[func_name] = {
                    "return_type": return_type.strip(),
                    "parameters": [
                        p.strip()
                        for p in params.split(",")
                        if p.strip()
                    ],
                    "header": filename
                }

        except Exception as e:

            print(
                f"Failed: {filepath}"
            )

    return contracts
    
#For testing purpose
if __name__ == "__main__":

    from context_builder import (
        discover_application_files
    )

    files = discover_application_files(
        "../HVAC_Project"
    )

    contracts = build_interface_contracts(
        files
    )

    from pprint import pprint

    pprint(contracts)
