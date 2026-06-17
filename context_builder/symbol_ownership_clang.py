import os

from clang import cindex

from context_builder.engines.clang_engine import (
    ClangEngine
)

from utils.file_loader import (
    discover_application_files
)


def build_symbol_ownership_clang(
    project_root,
    include_paths,
    defines
):
    """
    Build symbol ownership map using Clang AST.

    Returns:
    {
        "functions": {
            "main": "main.c",
            "MotorController_Init": "motor_controller.c",
            ...
        }
    }
    """

    ownership = {
        "functions": {}
    }

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
                    ==
                    cindex.CursorKind.FUNCTION_DECL
                ):

                    if (
                        cursor.is_definition()
                        and
                        cursor.location.file
                    ):

                        owner_file = os.path.basename(
                            cursor.location.file.name
                        )

                        # Keep only functions
                        # defined in the current source file
                        if owner_file == source_file:

                            ownership[
                                "functions"
                            ][
                                cursor.spelling
                            ] = owner_file

        except Exception as e:

            print(
                f"Clang failed: {file_path}"
            )

            print(e)

    return ownership
