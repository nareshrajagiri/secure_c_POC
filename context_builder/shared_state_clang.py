import os

from clang import cindex

from context_builder.engines.clang_engine import (
    ClangEngine
)

from utils.file_loader import (
    discover_application_files
)


def build_shared_state_clang(
    project_root,
    include_paths,
    defines
):
    """
    Build shared state map using Clang AST.

    Returns:

    {
        "s_motor_state": {
            "defined_in": "motor_controller.c",
            "used_by": [
                "main.c"
            ],
            "type": "MotorState_t"
        }
    }
    """

    application_files = (
        discover_application_files(
            project_root
        )
    )

    engine = ClangEngine()

    global_variables = {}

    #
    # Pass-1
    # Collect all global variables
    #

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

                #
                # Global variables only
                #

                if (
                    cursor.semantic_parent.kind
                    ==
                    cindex.CursorKind.TRANSLATION_UNIT
                ):

                    global_variables[
                        cursor.spelling
                    ] = {

                        "defined_in":
                            owner_file,

                        "type":
                            cursor.type.spelling,

                        "used_by":
                            []
                    }

        except Exception as e:

            print(
                f"Clang failed: {file_path}"
            )

            print(e)

    #
    # Pass-2
    # Find variable references
    #

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

            used_in_file = set()

            for cursor in tu.cursor.walk_preorder():

                if (
                    cursor.kind
                    !=
                    cindex.CursorKind.DECL_REF_EXPR
                ):
                    continue

                variable_name = (
                    cursor.spelling
                )

                if (
                    variable_name
                    not in
                    global_variables
                ):
                    continue

                if (
                    global_variables[
                        variable_name
                    ][
                        "defined_in"
                    ]
                    ==
                    source_file
                ):
                    continue

                used_in_file.add(
                    variable_name
                )

            for variable_name in used_in_file:

                global_variables[
                    variable_name
                ][
                    "used_by"
                ].append(
                    source_file
                )

        except Exception:

            pass

    #
    # Keep only truly shared variables
    #

    shared_state = {}

    for (
        variable,
        info
    ) in global_variables.items():

        if info["used_by"]:

            shared_state[
                variable
            ] = info

    return shared_state
