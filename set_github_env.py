import requests
import base64
from github import Github

# === Konfiguration ===
GITHUB_REPO = "Rabbit-Fur/GGW-FUR-SYSTEM"
GITHUB_TOKEN = "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"

SECRETS_AND_VARS = {
    "GITHUB_REPO": "Rabbit-Fur/GGW-FUR-SYSTEM",
    "GITHUB_TOKEN": "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",
    "DISCORD_TOKEN": "MTM2Mjg4ODY4ODk5MTczMTk2Mw.GVshnj.eTNdMbQZWtjRR2erOWEwTxDNSMPmcD-Thpa7Gc",
    "DISCORD_CLIENT_ID": "136288868899173196",
    "DISCORD_CLIENT_SECRET": "FqVmNprfXB_J15hBpgU-rXHGqBB9jvDB",
    "DISCORD_GUILD_ID": "1344968805151019088",
    "DISCORD_CHANNEL_ID": "1365580225945014385",
    "DISCORD_ADMIN_ROLE_ID": "1345007778871115846",
    "ADMIN_ROLE_IDS": "1345008298528604231",
    "R4_ROLE_IDS": "1345008234527723520",
    "R3_ROLE_IDS": "1345008403059179570",
    "BASE_URL": "https://system-by-fur.up.railway.app/",
    "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/1363796827316420809/W7YjDFdVRcazdjranKBjHgQFY4KNTo578_wUhRCXZTk4leuMalPxnji33BzElz4eua-w",
    "DISCORD_REDIRECT_URI": "https://system-by-fur.up.railway.app//callback",
    "SESSION_SECRET": "4fa028caf6d5c91645e37d8ce1400ec1451285bcceafaa3ccf273fcb3396f913",
    "GOOGLE_CLIENT_ID": "858610490497-6l1rp8bo51e7sd3pmklhpmbcrf9bfbft.apps.googleusercontent.com",
    "GOOGLE_PROJECT_ID": "erudite-fusion-456918-h4",
    "GOOGLE_CLIENT_SECRET": "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",
    "GOOGLE_AUTH_URI": "https://accounts.google.com/o/oauth2/auth",
    "GOOGLE_TOKEN_URI": "https://oauth2.googleapis.com/token",
    "GOOGLE_AUTH_PROVIDER_CERT_URL": "https://www.googleapis.com/v1/certs",
    "GOOGLE_REDIRECT_URI": "http://localhost"
}

# === GitHub Auth via REST (für Secrets & Vars) ===
owner, repo_name = GITHUB_REPO.split("/")
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# === Public Key holen (für Secrets verschlüsseln) ===
key_url = f"https://api.github.com/repos/{owner}/{repo_name}/actions/secrets/public-key"
key_resp = requests.get(key_url, headers=headers)
key_data = key_resp.json()
public_key = key_data["key"]
key_id = key_data["key_id"]

# === Helper zum Verschlüsseln der Secrets ===
def encrypt_secret(public_key: str, secret_value: str) -> str:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    import nacl.encoding
    import nacl.public

    public_key = nacl.public.PublicKey(public_key.encode("utf-8"), encoding=nacl.encoding.Base64Encoder())
    sealed_box = nacl.public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

# === Secrets setzen (verschlüsselt)
for key, value in SECRETS_AND_VARS.items():
    encrypted = encrypt_secret(public_key, value)
    secret_url = f"https://api.github.com/repos/{owner}/{repo_name}/actions/secrets/{key}"
    response = requests.put(
        secret_url,
        headers=headers,
        json={
            "encrypted_value": encrypted,
            "key_id": key_id
        }
    )
    print(f"🔐 Secret {key}: {response.status_code}")

# === Repo-Variablen setzen (nicht verschlüsselt)
vars_url = f"https://api.github.com/repos/{owner}/{repo_name}/actions/variables"
for key, value in SECRETS_AND_VARS.items():
    var_resp = requests.put(
        f"{vars_url}/{key}",
        headers=headers,
        json={"name": key, "value": value}
    )
    print(f"📦 Variable {key}: {var_resp.status_code}")
