import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict
import openai

# === Konfiguration ===
LANG_DIR = "i18n"
MASTER_LANG = "de"
REPORT_PATH = "untranslated_report.md"
USE_GPT = True

# 🌍 32 meistgesprochene Sprachen (ISO 639-1)
TARGET_LANGS = [
    "zh", "es", "en", "hi", "ar", "bn", "pt", "ru", "ja", "pa",
    "de", "jv", "ko", "fr", "te", "mr", "tr", "ta", "vi", "ur",
    "it", "fa", "pl", "uk", "nl", "th", "gu", "ro", "hu", "id",
    "sv", "cs"
]

# GPT-Key laden
openai.api_key = os.getenv("OPENAI_API_KEY")
if USE_GPT and not openai.api_key:
    raise EnvironmentError("❌ OPENAI_API_KEY ist nicht gesetzt.")


def extract_placeholders(text):
    return re.findall(r"{[^{}]+}", text)


def restore_placeholders(translated, original_placeholders):
    found = extract_placeholders(translated)
    for i, ph in enumerate(found):
        if i < len(original_placeholders):
            translated = translated.replace(ph, original_placeholders[i], 1)
    return translated


def translate(text, lang):
    placeholders = extract_placeholders(text)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Übersetze folgenden Text ins {lang} für eine Benutzeroberfläche. "
                           f"Behalte Platzhalter wie {{name}}, {{count}} unverändert:\n\n'{text}'"
            }],
            temperature=0.3
        )
        result = response.choices[0].message.content.strip()
        return restore_placeholders(result, placeholders)
    except Exception as e:
        print(f"⚠️ GPT-Fehler ({lang}): {e}")
        return f"[{lang}] {text}"


def load_json(path):
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Ungültige JSON-Datei: {path}")
        return {}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def sync_translations(dry_run=False, report_only=False):
    base_path = Path(LANG_DIR)
    master_path = base_path / f"{MASTER_LANG}.json"
    master_data = load_json(master_path)

    report = defaultdict(list)

    for lang in TARGET_LANGS:
        if lang == MASTER_LANG:
            continue

        target_path = base_path / f"{lang}.json"
        target_data = load_json(target_path)

        updated = False

        for key, value in master_data.items():
            if key not in target_data or not target_data[key]:
                translated = translate(value, lang)
                target_data[key] = translated
                report[lang].append(key)
                updated = True

        if updated and not dry_run and not report_only:
            save_json(target_path, target_data)

    return report


def generate_report(report):
    lines = ["# Übersetzungs-Report\n"]
    for lang, keys in report.items():
        lines.append(f"## {lang} ({len(keys)} neu)")
        lines.extend([f"- {key}" for key in keys])
        lines.append("")
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronisiere i18n JSON-Dateien in mehrere Sprachen.")
    parser.add_argument("--dry-run", action="store_true", help="Zeigt nur, was geändert würde.")
    parser.add_argument("--report-only", action="store_true", help="Erstellt nur den Report, ohne zu übersetzen.")
    args = parser.parse_args()

    print("🌍 Starte Übersetzungsabgleich...")

    result = sync_translations(dry_run=args.dry_run, report_only=args.report_only)
    generate_report(result)

    print(f"✅ Fertig. Report: {REPORT_PATH}")
    if args.dry_run:
        print("⚠️ Dry-Run: Keine Dateien wurden verändert.")
    elif args.report_only:
        print("📄 Nur Report erstellt – Übersetzung übersprungen.")
