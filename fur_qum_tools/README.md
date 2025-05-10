# FUR QUM Tools – API & GPT Integration

Dieses Verzeichnis enthält die OpenAPI-Spezifikationen und Umgebungsdaten für die GPT-Integration von FUR QUM.

## 🛠️ Dateien

- `github_openapi.json` – Zugriff auf GitHub Repos
- `railway_openapi.json` – Zugriff auf Railway Deployments
- `.env.example` – Platzhalter für lokale oder CI/CD Nutzung
- `.env.schema.json` – Validierung für GPTs oder CLI Tools
- `tool_*.yaml` – Optional für LangChain oder AgentTools

## 🚀 Nutzung mit ChatGPT Custom GPT

1. Gehe zu https://platform.openai.com/gpts
2. Öffne deinen GPT
3. Wähle „Aktionen hinzufügen“
4. Importiere die JSON-Dateien über ihre RAW-URLs:

