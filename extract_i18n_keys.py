import json
import os
import re
from pathlib import Path
import openai

# === Konfiguration ===
SOURCE_DIRS = [".", "templates"]
TARGET_LANG = "de"
TRANSLATION_FILE = Path(f"translations/{TARGET_LANG}.json")
USE_GPT = True

# === API Key setzen ===
openai.api_key = os.getenv("OPENAI_API_KEY")
if USE_GPT and not openai.api_key:
    raise EnvironmentError("❌ OPENAI_API_KEY ist nicht gesetzt.")


def scan_translation_keys():
    """
    Scannt alle Quellverzeichnisse nach _('Text')-Keys und gibt eine sortierte Liste zurück.
    """
    pattern = re.compile(r"_\(\s*['\"](.+?)['\"]\s*\)")
    found_keys = set()

    for folder in SOURCE_DIRS:
        for path in Path(folder).rglob("*"):
            if path.suffix in {".py", ".html", ".jinja", ".jinja2"} and path.is_file():
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                    matches = pattern.findall(content)
                    if matches:
                        found_keys.update(matches)
                except Exception as e:
                    print(f"⚠️ Fehler beim Lesen von {path}: {e}")
    return sorted(found_keys)


def translate_gpt(text: str) -> str:
    """
    Übersetzt einen String ins Deutsche via OpenAI GPT.
    """
    try:
        print(f"🌍 GPT übersetzt: '{text}'")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Übersetze folgenden Text für eine Benutzeroberfläche ins Deutsche: '{text}'"}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ GPT-Fehler bei '{text}': {e}")
        return text


def update_translation_file(keys):
    """
    Aktualisiert oder erzeugt die JSON-Datei mit allen Keys.
    """
    TRANSLATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = {}

    if TRANSLATION_FILE.exists():
        with TRANSLATION_FILE.open(encoding="utf-8") as f:
            existing = json.load(f)

    new_count = 0
    for key in keys:
        if key not in existing:
            existing[key] = translate_gpt(key) if USE_GPT else key
            new_count += 1

    with TRANSLATION_FILE.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"✅ {new_count} neue Übersetzungen hinzugefügt.")
    print(f"📁 Datei gespeichert: {TRANSLATION_FILE}")


if __name__ == "__main__":
    print("🔍 Scanne Quellverzeichnisse nach _('...') Keys ...")
    keys = scan_translation_keys()
    print(f"🔑 {len(keys)} eindeutige Keys gefunden.")
    update_translation_file(keys)
