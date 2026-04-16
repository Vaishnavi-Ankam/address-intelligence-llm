from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "data/raw",
        "data/processed",
        "artifacts/models",
        "artifacts/evaluation",
        "artifacts/logs",
        "tests",
    ]:
        path = root / rel
        path.mkdir(parents=True, exist_ok=True)
        keep = path / ".gitkeep"
        keep.touch(exist_ok=True)
    print("Repository folders verified.")


if __name__ == "__main__":
    main()
