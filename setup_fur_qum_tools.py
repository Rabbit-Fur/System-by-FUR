import os

BASE_DIR = "fur_qum_tools"
os.makedirs(BASE_DIR, exist_ok=True)

def write_file(filename, content):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Datei erstellt: {path}")

# env_openapi.yaml
write_file("env_openapi.yaml", """openapi: 3.1.0
info:
  title: FUR QUM Env API
  version: 1.0.0
  description: Validiert Umgebungsvariablen für das System-by-FUR Projekt
servers:
  - url: https://api.system-by-fur.dev
    description: Hauptserver für Umgebungsvalidierung
paths:
  /env/validate:
    post:
      operationId: validateEnv
      summary: Validiert Umgebungsvariablen gegen das FUR QUM Schema
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EnvSchema'
      responses:
        '200':
          description: Validierung erfolgreich
          content:
            application/json:
              schema:
                type: object
                properties:
                  valid:
                    type: boolean
                    example: true
        '400':
          description: Validierungsfehler
          content:
            application/json:
              schema:
                type: object
                properties:
                  valid:
                    type: boolean
                    example: false
                  errors:
                    type: array
                    items:
                      type: string
components:
  schemas:
    EnvSchema:
      type: object
      required: [GITHUB_REPO, GITHUB_TOKEN, DISCORD_TOKEN, DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET,
                 DISCORD_GUILD_ID, DISCORD_CHANNEL_ID, DISCORD_ADMIN_ROLE_ID, ADMIN_ROLE_IDS, R4_ROLE_IDS,
                 R3_ROLE_IDS, DISCORD_REDIRECT_URI, DISCORD_WEBHOOK_URL, BASE_URL, SESSION_SECRET,
                 GOOGLE_CLIENT_ID, GOOGLE_PROJECT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_AUTH_URI,
                 GOOGLE_TOKEN_URI, GOOGLE_AUTH_PROVIDER_CERT_URL, GOOGLE_REDIRECT_URI]
      properties:
        GITHUB_REPO: {type: string, pattern: ^.+/.+$}
        GITHUB_TOKEN: {type: string, minLength: 30}
        DISCORD_TOKEN: {type: string, minLength: 30}
        DISCORD_CLIENT_ID: {type: string}
        DISCORD_CLIENT_SECRET: {type: string}
        DISCORD_GUILD_ID: {type: string}
        DISCORD_CHANNEL_ID: {type: string}
        DISCORD_ADMIN_ROLE_ID: {type: string}
        ADMIN_ROLE_IDS: {type: string}
        R4_ROLE_IDS: {type: string}
        R3_ROLE_IDS: {type: string}
        DISCORD_REDIRECT_URI: {type: string, format: uri}
        DISCORD_WEBHOOK_URL: {type: string, format: uri}
        BASE_URL: {type: string, format: uri}
        SESSION_SECRET: {type: string, minLength: 32}
        GOOGLE_CLIENT_ID: {type: string}
        GOOGLE_PROJECT_ID: {type: string}
        GOOGLE_CLIENT_SECRET: {type: string}
        GOOGLE_AUTH_URI: {type: string, format: uri}
        GOOGLE_TOKEN_URI: {type: string, format: uri}
        GOOGLE_AUTH_PROVIDER_CERT_URL: {type: string, format: uri}
        GOOGLE_REDIRECT_URI: {type: string, format: uri}
""")

# tool_env.yaml
write_file("tool_env.yaml", """name_for_model: env_validator
name_for_human: Umgebungsvariablen-Validierung
description_for_model: "Validiere eine .env-Datei gegen das erwartete Schema"
description_for_human: "Prüfe, ob deine Umgebungsvariablen vollständig und korrekt sind."

api:
  type: openapi
  url: https://raw.githubusercontent.com/Rabbit-Fur/System-by-FUR/main/fur-qum-tools/env_openapi.yaml
  is_user_authenticated: false
""")

# tool_github.yaml
write_file("tool_github.yaml", """name_for_model: github_agent
name_for_human: GitHub API Zugriff
description_for_model: "Zugriff auf GitHub-Repos und Metadaten"
description_for_human: "Hole dir Repos, Commits oder öffne Issues über die GitHub API."

api:
  type: openapi
  url: https://raw.githubusercontent.com/Rabbit-Fur/System-by-FUR/main/fur-qum-tools/github_openapi.json
  is_user_authenticated: true
auth:
  type: bearer
  authorization_type: header
  verification_tokens:
    openai: dein-token
""")

# tool_railway.yaml
write_file("tool_railway.yaml", """name_for_model: railway_agent
name_for_human: Railway Deployment Tool
description_for_model: "Zugriff auf Railway-Projekte, Deployments und Logs"
description_for_human: "Verwalte Deployments und Umgebungen mit Railway."

api:
  type: openapi
  url: https://raw.githubusercontent.com/Rabbit-Fur/System-by-FUR/main/fur-qum-tools/railway_openapi.json
  is_user_authenticated: true
auth:
  type: bearer
  authorization_type: header
  verification_tokens:
    openai: dein-token
""")

# tool_branch_rules.yaml
write_file("tool_branch_rules.yaml", """name_for_model: github_branch_rules
name_for_human: GitHub Regelsatz-Analyse
description_for_model: "Analysiere Branchschutz und Pull-Request-Regeln über die GitHub API"
description_for_human: "Erkenne automatisch, welche Regeln für einen Branch aktiv sind. Ideal zur Push-Fehleranalyse oder Sicherheitsprüfung."

api:
  type: openapi
  url: https://raw.githubusercontent.com/Rabbit-Fur/System-by-FUR/main/fur-qum-tools/github-branch-rules/github_branch_rules_openapi.json
  is_user_authenticated: true

auth:
  type: bearer
  authorization_type: header
  verification_tokens:
    openai: dein-openai-verification-token
""")

# prompt_branch_rules.txt
write_file("prompt_branch_rules.txt", """🧠 GPT-Verhaltensmodul – GitHub Regelsatz-Diagnose

Wenn ein Push-Vorgang fehlschlägt oder du ein Repository analysierst, verwende folgendes Verfahren:

1. Rufe mit der API `/repos/{owner}/{repo}/branches/{branch}/protection` die aktiven Branchschutzregeln ab.
2. Ermittle:
   – Ob signierte Commits erforderlich sind
   – Ob PRs Reviews erfordern
   – Ob Force Pushes verboten sind
   – Ob Push nur für bestimmte Nutzer erlaubt ist
3. Antworte dem User strukturiert:
   – ❌ Was hat den Push blockiert?
   – 🔍 Welche GitHub-Regeln waren aktiv?
   – ✅ Wie kann man korrekt pushen oder umgehen?
   – 🛠 Falls Admin: Vorschlag zur Regelanpassung
""")

print("\n🎉 Alle Dateien wurden erfolgreich im Ordner 'fur_qum_tools' erstellt.")
