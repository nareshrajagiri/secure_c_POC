import os

from clang import cindex

from context_builder.engines.clang_engine import (
    ClangEngine
)

from utils.file_loader import (
    discover_application_files
)


def build_interface_contracts_clang(
    project_root,
    include_paths,
    defines
):
    """
    Extract API contracts from application header files.

    Returns:

    {
        "MotorController_Init": {
            "return_type": "void",
            "parameters": []
        },

        "MotorController_MoveTo": {
            "return_type": "void",
            "parameters": [
                {
                    "name": "target_position",
                    "type": "uint16_t"
                }
            ]
        }
    }
    """

    contracts = {}

    engine = ClangEngine()
    
    application_files = (
    discover_application_files(
        project_root
    )
)

    for file_path in application_files:

        if not file_path.endswith(".h"):
            continue

        try:

            tu = engine.parse_file(
                file_path,
                include_paths,
                defines
            )

            absolute_header = os.path.abspath(
                file_path
            )

            for cursor in tu.cursor.walk_preorder():

                # ----------------------------------
                # Only Function Declarations
                # ----------------------------------

                if (
                    cursor.kind
                    !=
                    cindex.CursorKind.FUNCTION_DECL
                ):
                    continue

                # ----------------------------------
                # Ignore functions coming from
                # STM32 HAL/CMSIS headers
                # ----------------------------------

                if not cursor.location.file:
                    continue

                cursor_file = os.path.abspath(
                    cursor.location.file.name
                )

                if cursor_file != absolute_header:
                    continue

                # ----------------------------------
                # Skip definitions
                # Keep only interface declarations
                # ----------------------------------

                if cursor.is_definition():
                    continue

                parameters = []

                for arg in cursor.get_arguments():

                    parameters.append(
                        {
                            "name": arg.spelling,
                            "type": arg.type.spelling
                        }
                    )

                contracts[
                    cursor.spelling
                ] = {
                    "return_type":
                        cursor.result_type.spelling,

                    "parameters":
                        parameters
                }

        except Exception as e:

            print(
                f"Clang failed: {file_path}"
            )

            print(e)

    return contracts
