import os
import requests

# === Konfiguration ===
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL") or "https://discord.com/api/webhooks/DEIN_WEBHOOK"

# Champion-Daten
image_path = "static/champions/champion_testchampion_mai2025.png"
champion_name = "TestChampion"
champion_title = "🔥 Champion of Unity 🔥"
month = "Mai 2025"

# === Prüfung auf Webhook-URL
if not WEBHOOK_URL or "DEIN_WEBHOOK" in WEBHOOK_URL:
    print("❌ Bitte setze eine gültige DISCORD_WEBHOOK_URL in deiner .env oder direkt im Code.")
    exit(1)

# === Bild prüfen
if not os.path.exists(image_path):
    print("❌ Bild nicht gefunden:", image_path)
    exit(1)

# === Nachricht vorbereiten
payload = {
    "content": f"🏆 **{champion_name}** wurde als Champion für **{month}** ausgezeichnet!\n{champion_title}"
}

# === Bild anhängen & senden
with open(image_path, "rb") as f:
    files = {"file": (os.path.basename(image_path), f)}
    response = requests.post(WEBHOOK_URL, data=payload, files=files)

# === Antwort prüfen
if response.status_code == 204:
    print("✅ Champion-Poster erfolgreich an Discord gesendet.")
else:
    print(f"❌ Fehler beim Senden: [{response.status_code}] {response.text}")
