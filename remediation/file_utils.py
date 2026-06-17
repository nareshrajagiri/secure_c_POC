# file_utils.py

from pathlib import Path

def save_text(content, path):

    Path(path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)