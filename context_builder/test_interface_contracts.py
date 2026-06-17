from utils.file_loader import (
    discover_application_files
)

from context_builder.discovery.include_discovery import (
    discover_include_paths
)

from context_builder.discovery.compiler_flag_discovery import (
    discover_compiler_flags
)

from context_builder.interface_contracts_clang import (
    build_interface_contracts_clang
)

project_root = r"C:\Users\nares\OneDrive\Desktop\Secure_C_POC\HVAC_Project"
application_files = discover_application_files(
    project_root
)

include_paths = discover_include_paths(
    project_root
)

flags = discover_compiler_flags(
    f"{project_root}/Debug"
)

contracts = build_interface_contracts_clang(
    application_files,
    include_paths,
    flags["defines"]
)

from pprint import pprint

pprint(contracts)
