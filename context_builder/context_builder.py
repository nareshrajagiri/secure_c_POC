import os
import json

from .dependency_graph import build_dependency_graph
from .symbol_ownership import build_symbol_ownership
from .interface_contracts import build_interface_contracts
from .call_graph import build_call_graph
from .shared_state import build_shared_state_map
from .protected_regions import build_protected_regions
from .peripheral_ownership import build_peripheral_ownership

from .symbol_ownership_clang import (
    build_symbol_ownership_clang
)

from .interface_contracts_clang import (
    build_interface_contracts_clang
)

from .call_graph_clang import (
    build_call_graph_clang
)

from .shared_state_clang import (
    build_shared_state_clang
)

from .peripheral_ownership_clang import (
    build_peripheral_ownership_clang
)

from .discovery.include_discovery import (
    discover_include_paths
)

from .discovery.compiler_flag_discovery import (
    discover_compiler_flags
)


STM32_IGNORE_FILES = {
    "stm32f4xx_it.c",
    "stm32f4xx_it.h",
    "stm32f4xx_hal_conf.h",
    "stm32f4xx_hal_msp.c",
    "syscalls.c",
    "sysmem.c",
    "system_stm32f4xx.c"
}


def discover_application_files(project_root):

    app_files = []

    core_src = os.path.join(
        project_root,
        "Core",
        "Src"
    )

    core_inc = os.path.join(
        project_root,
        "Core",
        "Inc"
    )

    for folder in [core_src, core_inc]:

        if not os.path.exists(folder):
            continue

        for file in os.listdir(folder):

            if file in STM32_IGNORE_FILES:
                continue

            if file.endswith((".c", ".h")):

                app_files.append(
                    os.path.join(folder, file)
                )

    return sorted(app_files)
    
    
def build_context(project_root):

    files = discover_application_files(
        project_root
    )

    include_paths = discover_include_paths(
        project_root
    )

    flags = discover_compiler_flags(
        os.path.join(
            project_root,
            "Debug"
        )
    )

    defines = flags["defines"]
    print(defines)

    try:

        print(
            "Using Clang Context Builder...",
            flush=True
        )

        print(
            "\n[1/7] Building Dependency Graph...",
            flush=True
        )

        dependency_graph = build_dependency_graph(
            files
        )

        print(
            "      DONE",
            flush=True
        )

        print(
            "\n[2/7] Building Symbol Ownership...",
            flush=True
        )

        symbol_ownership = (
            build_symbol_ownership_clang(
                project_root,
                include_paths,
                defines
            )
        )

        print(
            "      DONE",
            flush=True
        )

        print(
            "\n[3/7] Building Interface Contracts...",
            flush=True
        )

        interface_contracts = (
            build_interface_contracts_clang(
                project_root,
                include_paths,
                defines
            )
        )

        print(
            "      DONE",
            flush=True
        )

        print(
            "\n[4/7] Building Call Graph...",
            flush=True
        )

        call_graph = (
            build_call_graph_clang(
                project_root,
                include_paths,
                defines
            )
        )

        print(
            "      DONE",
            flush=True
        )

        print(
            "\n[5/7] Building Shared State Map...",
            flush=True
        )

        shared_state_map = (
            build_shared_state_clang(
                project_root,
                include_paths,
                defines
            )
        )

        print(
            "      DONE",
            flush=True
        )

        print(
            "\n[6/7] Building Peripheral Ownership...",
            flush=True
        )

        peripheral_ownership = (
            build_peripheral_ownership_clang(
                project_root,
                include_paths,
                defines
            )
        )

        print(
            "      DONE",
            flush=True
        )

        print(
            "\n[7/7] Building Protected Regions...",
            flush=True
        )

        protected_regions = (
            build_protected_regions(
                files
            )
        )

        print(
            "      DONE\n",
            flush=True
        )

    except Exception as e:

        print(
            f"Clang failed: {e}",
            flush=True
        )

        print(
            "Falling back to regex...",
            flush=True
        )

        dependency_graph = (
            build_dependency_graph(
                files
            )
        )

        symbol_ownership = (
            build_symbol_ownership(
                files
            )
        )

        interface_contracts = (
            build_interface_contracts(
                files
            )
        )

        call_graph = (
            build_call_graph(
                files
            )
        )

        shared_state_map = (
            build_shared_state_map(
                files
            )
        )

        protected_regions = (
            build_protected_regions(
                files
            )
        )

        peripheral_ownership = (
            build_peripheral_ownership(
                files
            )
        )

    context = {

        "dependency_graph":
            dependency_graph,

        "symbol_ownership":
            symbol_ownership,

        "interface_contracts":
            interface_contracts,

        "call_graph":
            call_graph,

        "shared_state_map":
            shared_state_map,

        "protected_regions":
            protected_regions,

        "peripheral_ownership":
            peripheral_ownership
    }

    return context
    
#For Testing purpose
if __name__ == "__main__":

    project_path = r"C:\Users\nares\OneDrive\Desktop\Secure_C_POC\HVAC_Project"

    context = build_context(
        project_path
    )

    with open(
        "context.json",
        "w"
    ) as f:

        json.dump(
            context,
            f,
            indent=4
        )

    print(
        "\nContext Generated Successfully\n"
    )

    print(
        "Output File: context.json"
    )
