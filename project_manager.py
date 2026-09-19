import json
from pathlib import Path

PROJECT_FILE = Path("projects.json")

def load_files():
    if not PROJECT_FILE.exists():
        return []


    try:
        with PROJECT_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("files", [])
    
    except (json.JSONDecodeError, IOError):
        return []

def save_files(files):
    data = {"files": files}

    with PROJECT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)