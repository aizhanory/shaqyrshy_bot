import json
from typing import Any


# Reads JSON file
def read_json(file_path: str) -> list[Any]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Writes data to JSON file with UTF-8 encoding
def write_json(file_path: str, data: list[Any]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)