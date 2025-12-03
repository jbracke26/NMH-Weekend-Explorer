import os
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "app" / "activities.json"


def init_db():
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


if __name__ == "__main__":
    init_db()
    print(f"Initialized {DATA_FILE}")
