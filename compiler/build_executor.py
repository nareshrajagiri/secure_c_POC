import os
import subprocess
from pathlib import Path

from compiler.compiler_config import (
    MAKE_PATH,
    GCC_BIN_PATH
)


def run_build(build_project_path: str):
    """
    Compile STM32 project using Makefile.
    """

    debug_dir = Path(build_project_path) / "Debug"

    output_dir = Path("compiler/outputs")
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    build_log_path = output_dir / "build.log"

    env = os.environ.copy()

    env["PATH"] = (
        GCC_BIN_PATH
        + os.pathsep
        + env["PATH"]
    )

    print(f"Build Directory : {debug_dir}")
    print("Running make clean...")

    clean_result = subprocess.run(
        [MAKE_PATH, "clean"],
        cwd=debug_dir,
        env=env,
        capture_output=True,
        text=True
    )

    print("Running make all...")

    build_result = subprocess.run(
        [MAKE_PATH, "all"],
        cwd=debug_dir,
        env=env,
        capture_output=True,
        text=True
    )

    full_log = (
        "\n=== MAKE CLEAN ===\n"
        + clean_result.stdout
        + clean_result.stderr
        + "\n\n=== MAKE ALL ===\n"
        + build_result.stdout
        + build_result.stderr
    )

    build_log_path.write_text(
        full_log,
        encoding="utf-8"
    )

    return {
    "success": build_result.returncode == 0,
    "return_code": build_result.returncode,
    "build_log": str(build_log_path),
    "stdout": build_result.stdout,
    "stderr": build_result.stderr
    }