import os
import json
from typing import Any

# Resolve project root and data dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _file_path(filename: str) -> str:
    _ensure_data_dir()
    return os.path.join(DATA_DIR, filename)


def load_json(filename: str, default: Any):
    """
    Load JSON from data/<filename>. If file is missing or invalid, return default.
    """
    path = _file_path(filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        # Keep it simple for the lab: treat malformed as empty default
        return default


def save_json(filename: str, data: Any) -> None:
    """
    Save data to data/<filename> with pretty formatting.
    """
    path = _file_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def next_id(items: list[dict]) -> int:
    """
    Given a list of dicts with 'id' keys, return the next integer id.
    """
    if not items:
        return 1
    return max((item.get("id", 0) for item in items), default=0) + 1
