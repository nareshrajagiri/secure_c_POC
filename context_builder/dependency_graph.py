import re


def build_dependency_graph(application_files):

    dependency_graph = {}

    include_pattern = re.compile(
        r'#include\s+"([^"]+)"'
    )

    for filepath in application_files:

        filename = filepath.split("/")[-1]

        try:

            with open(
                filepath,
                "r",
                errors="ignore"
            ) as f:

                content = f.read()

            includes = include_pattern.findall(
                content
            )

            dependency_graph[filename] = includes

        except Exception as e:

            print(
                f"Failed: {filepath}"
            )

    return dependency_graph
    
#For Testing purpose
if __name__ == "__main__":

    from context_builder import (
        discover_application_files
    )

    project_path = "../HVAC_Project"

    files = discover_application_files(
        project_path
    )

    graph = build_dependency_graph(files)

    from pprint import pprint

    pprint(graph)
