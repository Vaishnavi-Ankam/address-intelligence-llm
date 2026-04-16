import json
from pathlib import Path


def notebook_inventory(nb_path: Path):
    data = json.loads(nb_path.read_text(encoding="utf-8"))
    return {
        "file": nb_path.name,
        "cells": len(data.get("cells", [])),
        "markdown_cells": sum(1 for c in data.get("cells", []) if c.get("cell_type") == "markdown"),
        "code_cells": sum(1 for c in data.get("cells", []) if c.get("cell_type") == "code"),
    }


def main():
    notebooks_dir = Path(__file__).resolve().parents[1] / "notebooks"
    for nb in sorted(notebooks_dir.glob("*.ipynb")):
        print(notebook_inventory(nb))


if __name__ == "__main__":
    main()
