
import json
import os
import re
from pathlib import Path

import openai

SOURCE_DIRS = [".", "templates"]
TARGET_LANG = "de"
TRANSLATION_FILE = f"translations/{TARGET_LANG}.json"
USE_GPT = True  # GPT-Modus aktiviert

openai.api_key = os.getenv("OPENAI_API_KEY")


def scan_files():
    pattern = re.compile(r"_\(\s*["\'](.+?)["\']\\s*\\)")
    keys = set()

    for folder in SOURCE_DIRS:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith((".py", ".html", ".jinja", ".jinja2")):
                    with open(os.path.join(root, file), encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        keys.update(pattern.findall(content))
    return sorted(keys)


def gpt_de(text):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Übersetze folgenden Text ins Deutsch für eine UI: '{text}'"}],
            temperature=0.3)
        return res.choices[0].message.content.strip()
    except Exception:
        return text


def write_json(new_keys):
    existing = {}
    if os.path.exists(TRANSLATION_FILE):
        with open(TRANSLATION_FILE, encoding="utf-8") as f:
            existing = json.load(f)

    for key in new_keys:
        if key not in existing:
            existing[key] = gpt_de(key) if USE_GPT else key

    with open(TRANSLATION_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print("🔍 Scanne nach _() Keys ...")
    keys = scan_files()
    print(f"➕ {len(keys)} eindeutige Keys gefunden.")
    write_json(keys)
    print(f"✅ {TRANSLATION_FILE} aktualisiert.")
