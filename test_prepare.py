from compiler.project_preparer import prepare_build_project

path = prepare_build_project(
    project_path="HVAC_Project_Vulnerable",
    remediated_files_dir="outputs/remediated_files",
    build_root="outputs/build_project"
)

print(path)