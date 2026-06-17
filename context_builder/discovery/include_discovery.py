import os


def discover_include_paths(project_root):

    include_paths = []

    for root, dirs, files in os.walk(project_root):

        folder = os.path.basename(root)

        if folder in ["Inc", "Include"]:

            include_paths.append(root)

    return sorted(
        list(set(include_paths))
    )
