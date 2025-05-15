# 📦 GitHub Branch Rule Tool – FUR QUM Integration

Dieses Tool erlaubt deinem GPT, per OpenAPI die Branchschutzregeln eines GitHub-Repositories zu analysieren.

## 🔧 Nutzung im GPT Builder

1. Öffne deinen GPT in https://platform.openai.com/gpts
2. Gehe zu → „Aktionen > Aktionen hinzufügen“
3. Importiere das Schema:
   https://raw.githubusercontent.com/Rabbit-Fur/System-by-FUR/main/fur-qum-tools/github-branch-rules/github_branch_rules_openapi.json

## 🧠 GPT-Logik

Nutze den Prompt `prompt_branch_rules.txt`, um deinem GPT beizubringen:
– wie Branchschutz funktioniert
– wie man Push-Probleme automatisch erklärt
– wie Admins Regeln optimieren können

## ✅ Token-Anforderungen

- GitHub PAT mit Scope `repo` und optional `admin:repo_hook`
