
import os
import json
import glob
import re
from pathlib import Path
from collections import defaultdict

LANG_DIR = "i18n"
MASTER_LANG = "de"
TARGET_LANGS = ["en", "fr", "tr", "pl", "es", "it"]

USE_GPT = True
REPORT_PATH = "untranslated_report.md"

# === Platzhalter extrahieren ===


def extract_placeholders(text):
    return re.findall(r"{[^{}]+}", text)

# === Platzhalter wieder einsetzen ===


def restore_placeholders(translated, original_placeholders):
    found = extract_placeholders(translated)
    for i, ph in enumerate(found):
        if i < len(original_placeholders):
            translated = translated.replace(ph, original_placeholders[i])
    return translated

# === Übersetzungs-Strategie ===


def translate(text, lang):
    placeholders = extract_placeholders(text)
    if USE_GPT:
        # GPT- oder DeepL-/API-Integration hier einfügen
        translated = f"[GPT:{lang}] {text}"
    else:
        translated = fallback_translate(text, lang)
    return restore_placeholders(translated, placeholders)

# === Fallback: Dummy-Übersetzer ===


def fallback_translate(text, lang):
    return f"[{lang}] {text}"


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def sync_translations():
    base_path = Path(LANG_DIR)
    master_path = base_path / f"{MASTER_LANG}.json"
    master_data = load_json(master_path)

    report = defaultdict(list)

    for lang in TARGET_LANGS:
        target_path = base_path / f"{lang}.json"
        target_data = load_json(target_path)

        updated = False

        for key, value in master_data.items():
            if key not in target_data or not target_data[key]:
                translated = translate(value, lang)
                target_data[key] = translated
                report[lang].append(key)
                updated = True

        if updated:
            save_json(target_path, target_data)

    return report


def generate_report(report):
    lines = ["# Fehlende Übersetzungen synchronisiert\n"]
    for lang, keys in report.items():
        lines.append(f"## {lang} ({len(keys)} neue Keys)")
        for key in keys:
            lines.append(f"- {key}")
        lines.append("")
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    print("🌐 Übersetzungs-Sync gestartet...")
    result = sync_translations()
    generate_report(result)
    print("✅ Synchronisiert. Siehe:", REPORT_PATH)
