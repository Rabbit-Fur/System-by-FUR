import os
import re
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
IGNORED_DIRS = {"venv", ".venv", "__pycache__", "migrations"}

def fix_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"❌ Fehler beim Lesen von {filepath}: {e}")
        return

    new_lines = []
    for i, line in enumerate(lines):
        # E302/E305: Leerzeile vor Funktionen/Klassen
        if re.match(r"^def |^class ", line) and (i == 0 or lines[i - 1].strip()):
            new_lines.append("\n")

        # E261: 2 Leerzeichen vor Kommentar
        if "  #" in line and not line.lstrip().startswith("  #"):
            line = re.sub(r"([^\s])\s?  #", r"\1  #", line)

        # E265: Kommentar sollte mit "# " beginnen
        if re.match(r"^\s*  #\S", line):
            line = re.sub(r"^\s*  #", "  # ", line)

        new_lines.append(line)

    if new_lines and not new_lines[-1].endswith("\n"):
        new_lines[-1] += "\n"  # W292: newline am Ende

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"✅ Formatiert: {filepath}")
    except OSError as e:
        print(f"❌ Fehler beim Schreiben in {filepath}: {e}")


def run_flake8_and_fix():
    py_files = [
        file for file in PROJECT_DIR.rglob("*.py")
        if not any(part in IGNORED_DIRS for part in file.parts)
    ]

    print(f"🔧 Fixe {len(py_files)} Python-Dateien...")

    for file in py_files:
        fix_file(file)

    print("✅ Basis-Fixes abgeschlossen. Führe black & isort aus...")

    try:
        subprocess.run(["black", "."], cwd=PROJECT_DIR, check=True)
        subprocess.run(["isort", "."], cwd=PROJECT_DIR, check=True)
    except FileNotFoundError as e:
        print(f"❌ Werkzeug nicht gefunden (black/isort): {e}")


def fix_unused_imports():
    """Autoflake: entferne ungenutzte Imports & Variablen."""
    print("🧹 Entferne ungenutzte Importe mit autoflake...")
    try:
        subprocess.run(
            ["autoflake", "--in-place", "--remove-all-unused-imports", "--remove-unused-variables", "-r", "."],
            cwd=PROJECT_DIR,
            check=True
        )
    except FileNotFoundError:
        print("❌ 'autoflake' ist nicht installiert. Bitte via pip installieren: pip install autoflake")


if __name__ == "__main__":
    try:
        run_flake8_and_fix()
        fix_unused_imports()
        print("🎉 Code-Cleanup abgeschlossen.")
    except Exception as e:
        print(f"❌ Fehler beim automatischen Fix: {e}")
