import json
import re
from typing import Any


def safe_json_loads(text: str) -> Any:
    text = text.strip()
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        text = match.group(0)
    return json.loads(text)


def ensure_float(value, default=0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)
