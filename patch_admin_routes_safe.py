# patch_admin_routes_safe.py – Fügt Fallback für _() in admin/routes.py ein
from pathlib import Path

target = Path("admin/routes.py")
if not target.exists():
    print("❌ Datei admin/routes.py nicht gefunden.")
    exit(1)

code = target.read_text()
if "_(" in code and "from flask_babel import _" not in code:
    safe_patch = "try:\n    from flask_babel import _\nexcept ImportError:\n    _ = lambda x: x\n"
    code = safe_patch + code
    target.write_text(code)
    print("✅ Fallback für _() in admin/routes.py hinzugefügt.")
else:
    print("✅ Kein Patch notwendig – _() ist bereits sicher.")
