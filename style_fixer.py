import re
from pathlib import Path


def fix_css_file(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    fixed_lines = []
    brace_depth = 0
    properties_seen = set()

    for line in lines:
        stripped = line.rstrip()
        # Track CSS block depth
        if "{" in stripped:
            brace_depth += 1
            properties_seen.clear()
        if "}" in stripped:
            brace_depth = max(brace_depth - 1, 0)

        # Fix missing semicolon in property lines
        m = re.match(r"(\s*[\w-]+\s*:\s*[^;\{]+)(\s*)$", stripped)
        if m and brace_depth > 0:
            fixed_lines.append(m.group(1) + ";")
            continue

        # Remove duplicate properties in the same block
        if brace_depth > 0 and ":" in stripped and not stripped.startswith("@"):
            prop = stripped.split(":", 1)[0].strip()
            if prop in properties_seen:
                # Skip duplicate
                continue
            properties_seen.add(prop)

        fixed_lines.append(stripped)

    path.write_text("\n".join(fixed_lines), encoding="utf-8")


def main():
    for css_path in Path("static").rglob("*.css"):
        fix_css_file(css_path)
    print("✅ CSS-Fix abgeschlossen.")


if __name__ == "__main__":
    main()
