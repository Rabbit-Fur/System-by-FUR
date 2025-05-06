import os

import requests

# Webhook-URL (bitte setzen)
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL") or "https://discord.com/api/webhooks/DEIN_WEBHOOK"

# Bild und Nachricht
image_path = "static/champions/champion_testchampion_mai2025.png"
champion_name = "TestChampion"
champion_title = "🔥 Champion of Unity 🔥"
month = "Mai 2025"

# Nachricht
payload = {"content": f"🏆 **{champion_name}** wurde als Champion für **{month}** ausgezeichnet!\n{champion_title}"}

# Datei anhängen
if not os.path.exists(image_path):
    print("❌ Bild nicht gefunden:", image_path)
    exit(1)

with open(image_path, "rb") as f:
    files = {"file": (os.path.basename(image_path), f)}
    response = requests.post(WEBHOOK_URL, data=payload, files=files)

if response.status_code == 204:
    print("✅ Champion-Poster erfolgreich an Discord gesendet.")
else:
    print("❌ Fehler beim Senden:", response.status_code, response.text)
