import os

from clang import cindex

from context_builder.engines.clang_engine import (
    ClangEngine
)

from context_builder.symbol_ownership_clang import (
    build_symbol_ownership_clang
)

from utils.file_loader import (
    discover_application_files
)


def build_call_graph_clang(
    project_root,
    include_paths,
    defines
):
    """
    Build function call graph using Clang AST.

    Returns:

    {
        "MotorController_Update": [
            "PositionSensing_Update",
            "PositionSensing_IsAtTarget"
        ]
    }
    """

    call_graph = {}

    application_files = (
        discover_application_files(
            project_root
        )
    )

    engine = ClangEngine()
    
    ownership = build_symbol_ownership_clang(
    project_root,
    include_paths,
    defines
)

    application_functions = set(
    ownership["functions"].keys()
)

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
                    cindex.CursorKind.FUNCTION_DECL
                ):
                    continue

                if not cursor.is_definition():
                    continue

                if not cursor.location.file:
                    continue

                owner_file = os.path.basename(
                    cursor.location.file.name
                )

                if owner_file != source_file:
                    continue

                caller = cursor.spelling

                call_graph[caller] = []

                for child in cursor.walk_preorder():

                    if (
                        child.kind
                        ==
                        cindex.CursorKind.CALL_EXPR
                    ):

                        callee = child.spelling

                        if not callee:
                            continue

                        if (
                            callee
                            not in
                            application_functions
                        ):
                            continue

                        if (
                            callee
                            not in
                            call_graph[caller]
                        ):

                            call_graph[
                            caller
                            ].append(
                            callee
                            )

        except Exception as e:

            print(
                f"Clang failed: {file_path}"
            )

            print(e)

    return call_graph
