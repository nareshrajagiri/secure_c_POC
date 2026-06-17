import os
import re


def build_protected_regions(application_files):

    protected_regions = {
        "user_code_regions": {},
        "generated_functions": {}
    }

    #
    # Capture complete STM32 USER CODE markers
    #
    user_code_pattern = re.compile(
        r'USER CODE BEGIN\s+[^\r\n*]+'
    )

    generated_function_pattern = re.compile(
        r'\b(MX_[A-Za-z0-9_]+)\s*\('
    )

    for filepath in application_files:

        filename = os.path.basename(filepath)

        try:

            with open(
                filepath,
                "r",
                errors="ignore"
            ) as f:

                content = f.read()

            # ----------------------------------
            # USER CODE REGIONS
            # ----------------------------------

            regions = []

            for match in user_code_pattern.findall(
                content
            ):

                region = match.strip()

                if region not in regions:

                    regions.append(
                        region
                    )

            if regions:

                protected_regions[
                    "user_code_regions"
                ][filename] = regions

            # ----------------------------------
            # GENERATED FUNCTIONS
            # ----------------------------------

            generated_funcs = set(
                generated_function_pattern.findall(
                    content
                )
            )

            if generated_funcs:

                protected_regions[
                    "generated_functions"
                ][filename] = sorted(
                    list(generated_funcs)
                )

        except Exception:

            pass

    return protected_regions


if __name__ == "__main__":

    from context_builder import (
        discover_application_files
    )

    files = discover_application_files(
        "../HVAC_Project"
    )

    result = build_protected_regions(
        files
    )

    from pprint import pprint

    pprint(result)
