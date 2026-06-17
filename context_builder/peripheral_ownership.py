import os
import re


def build_peripheral_ownership(application_files):

    ownership = {}

    peripheral_patterns = {
        "ADC": r"\bhadc\d+\b",
        "TIM": r"\bhtim\d+\b",
        "USART": r"\bhuart\d+\b",
        "I2C": r"\bhi2c\d+\b",
        "SPI": r"\bhspi\d+\b",
        "CAN": r"\bhcan\d+\b"
    }

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

            for peripheral_type, pattern in peripheral_patterns.items():

                matches = re.findall(
                    pattern,
                    content
                )

                for match in matches:

                    ownership[match] = filename

        except Exception:

            pass

    return ownership


if __name__ == "__main__":

    from context_builder import (
        discover_application_files
    )

    files = discover_application_files(
        "../HVAC_Project"
    )

    result = build_peripheral_ownership(
        files
    )

    from pprint import pprint

    pprint(result)
