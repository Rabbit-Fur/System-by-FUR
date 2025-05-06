
import os
import re
from pathlib import Path
import subprocess

PROJECT_DIR = Path(__file__).resolve().parent


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
except OSError as e:
    print(f"Error reading file {filepath}: {e}")

        lines = f.readlines()

    new_lines = []
    import_lines = []
    in_import_block = False

    for i, line in enumerate(lines):
        # Track imports for F401 cleanup
        if re.match(r'^\s*(from\s+\S+\s+import|import\s+\S+)', line):
            in_import_block = True
            import_lines.append((i, line))
        else:
            in_import_block = False

        # Fix E302/E305 – insert blank lines before top-level defs
        if re.match(r'^def |^class ', line) and (i == 0 or lines[i-1].strip()):
            new_lines.append('\n')

        # Fix E261 – comments need 2 spaces before
        if '  #' in line and not line.lstrip().startswith('  #'):
            line = re.sub(r'([^\s])\s?  #', r'\1  #', line)

        # Fix E265 – block comment should start with '# '
        if re.match(r'^\s*  #\S', line):
            line = re.sub(r'^\s*  #', '  # ', line)

        new_lines.append(line)

    # Ensure final newline (W292)
    if new_lines and not new_lines[-1].endswith('\n'):
        new_lines[-1] += '\n'

    # Write back fixed version
    with open(filepath, 'w', encoding='utf-8') as f:
except OSError as e:
    print(f"Error reading file {filepath}: {e}")

        f.writelines(new_lines)


def run_flake8_and_fix():
    py_files = list(PROJECT_DIR.rglob('*.py'))
    print(f"🔧 Fixing {len(py_files)} Python files...")
    for file in py_files:
        if "venv" in str(file) or ".venv" in str(
                file) or "migrations" in str(file):
            continue
        fix_file(file)

    print("✅ Base formatting done. Running black and isort...")
    subprocess.run(["black", "."], cwd=PROJECT_DIR)
    subprocess.run(["isort", "."], cwd=PROJECT_DIR)
    print("✅ Auto-fix completed.")


if __name__ == "__main__":
    run_flake8_and_fix()

def fix_unused_imports():
    """Remove unused imports and variables across the project."""
    import subprocess
    print("Running autoflake to remove unused imports...")
    subprocess.run([
        "autoflake", "--in-place", "--remove-all-unused-imports",
        "--remove-unused-variables", "-r", "."
    ], check=True)

if __name__ == "__main__":
    # existing sync or main logic...
    try:
        fix_unused_imports()
    except Exception as e:
        print(f"Error during autoflake cleanup: {e}")
