import os
import shutil

# Files that should NEVER be remediated
EXCLUDED_SRC_FILES = {
    "stm32f4xx_hal_msp.c",
    "stm32f4xx_it.c",
    "syscalls.c",
    "sysmem.c",
    "system_stm32f4xx.c"
}

EXCLUDED_INC_FILES = {
    "stm32f4xx_hal_conf.h",
    "stm32f4xx_it.h"
}


def prepare_project_workspace(project_path):
    """
    Create workspace with:
    - original_project
    - remediated_project
    """

    workspace_root = "workspace"

    original_project = os.path.join(
        workspace_root,
        "original_project"
    )

    remediated_project = os.path.join(
        workspace_root,
        "remediated_project"
    )

    # Clean old workspace
    if os.path.exists(workspace_root):
        shutil.rmtree(workspace_root)

    os.makedirs(workspace_root, exist_ok=True)

    # Copy original project
    shutil.copytree(project_path, original_project)

    # Create working/remediation copy
    shutil.copytree(original_project, remediated_project)

    return {
        "workspace_root": workspace_root,
        "original_project": original_project,
        "remediated_project": remediated_project
    }


def discover_application_files(project_root):
    """
    Discover ONLY user application files.

    Include:
    - Core/Src/*.c
    - Core/Inc/*.h

    Exclude STM32 generated/system files.
    """

    application_files = []

    core_src = os.path.join(project_root, "Core", "Src")
    core_inc = os.path.join(project_root, "Core", "Inc")

    # Scan Core/Src
    if os.path.exists(core_src):

        for file in sorted(os.listdir(core_src)):

            if not file.endswith(".c"):
                continue

            if file in EXCLUDED_SRC_FILES:
                continue

            full_path = os.path.join(core_src, file)

            application_files.append(full_path)

    # Scan Core/Inc
    if os.path.exists(core_inc):

        for file in sorted(os.listdir(core_inc)):

            if not file.endswith(".h"):
                continue

            if file in EXCLUDED_INC_FILES:
                continue

            full_path = os.path.join(core_inc, file)

            application_files.append(full_path)

    return application_files
