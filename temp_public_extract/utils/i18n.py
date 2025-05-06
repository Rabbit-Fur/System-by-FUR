# --- START OF FILE utils/i18n.py ---
import json
import os


def get_translation(lang: str, key: str) -> str:
    path = os.path.join("translations", f"{lang}.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get(key, key)
    except FileNotFoundError:
        return key
# --- END OF FILE utils/i18n.py ---
