from pathlib import Path
import shutil


def prepare_build_project(
    project_path: str,
    remediated_files_dir: str,
    build_root: str
):
    """
    Creates a temporary build project and
    replaces source files with remediated versions.
    """

    project_path = Path(project_path)
    remediated_files_dir = Path(remediated_files_dir)

    build_root = Path(build_root)

    build_project_path = build_root / project_path.name

    # remove old build project
    if build_project_path.exists():
        shutil.rmtree(build_project_path)

    # copy project
    shutil.copytree(
        project_path,
        build_project_path
    )

    # replace files
    for file in remediated_files_dir.glob("*"):

        target = None

        if file.suffix == ".c":
            target = (
                build_project_path /
                "Core" /
                "Src" /
                file.name
            )

        elif file.suffix == ".h":
            target = (
                build_project_path /
                "Core" /
                "Inc" /
                file.name
            )

        if target and target.exists():
            shutil.copy2(file, target)

    return str(build_project_path)