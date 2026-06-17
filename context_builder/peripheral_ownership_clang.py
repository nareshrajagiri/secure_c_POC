import os

from clang import cindex

from context_builder.engines.clang_engine import (
    ClangEngine
)

from utils.file_loader import (
    discover_application_files
)


PERIPHERAL_TYPES = {

    "ADC_HandleTypeDef": "ADC",

    "TIM_HandleTypeDef": "TIM",

    "UART_HandleTypeDef": "USART",

    "I2C_HandleTypeDef": "I2C",

    "SPI_HandleTypeDef": "SPI",

    "CAN_HandleTypeDef": "CAN"
}


def build_peripheral_ownership_clang(
    project_root,
    include_paths,
    defines
):

    ownership = {}

    application_files = (
        discover_application_files(
            project_root
        )
    )

    engine = ClangEngine()

    for file_path in application_files:

        if not file_path.endswith(".c"):
            continue

        try:

            tu = engine.parse_file(
                file_path,
                include_paths,
                defines
            )

            source_file = os.path.basename(
                file_path
            )

            for cursor in tu.cursor.walk_preorder():

                if (
                    cursor.kind
                    !=
                    cindex.CursorKind.VAR_DECL
                ):
                    continue

                if not cursor.location.file:
                    continue

                owner_file = os.path.basename(
                    cursor.location.file.name
                )

                if owner_file != source_file:
                    continue

                var_type = (
                    cursor.type.spelling
                )

                if (
                    var_type
                    not in
                    PERIPHERAL_TYPES
                ):
                    continue

                ownership[
                    cursor.spelling
                ] = {

                    "type":
                        PERIPHERAL_TYPES[
                            var_type
                        ],

                    "owner":
                        owner_file
                }

        except Exception as e:

            print(
                f"Clang failed: {file_path}"
            )

            print(e)

    return ownership
