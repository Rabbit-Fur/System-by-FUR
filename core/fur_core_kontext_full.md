
# 🧠 FUR QUM – Gesamter Core-Kontext (100%)

Dies ist die vollständige und strukturierte Zusammenfassung aller Systemmodule, Technologien, Zustände, GPT-Erweiterungen und Projektziele aus dem aktiven Core-Kontext.

---

## 📦 1. Systemmodule & Technologien

### 🔧 Backend (Python)
- Flask Routing (Blueprints, Secure Sessions)
- APScheduler (Reminder Tasks)
- SQLAlchemy / sqlite3 (ORM & direkte Queries)
- PIL (Image Processing für Champion-Poster)
- dotenv (.env Konfiguration)
- Error-Logging (logging, atexit, signal)

### 🧠 GPT-Autopilot-Module
- Auto-Fixer v4 (AST-basiert, Docstrings, git-hooks)
- RAG-System (Retrieval-Augmented Generation mit 1000+ Modulen)
- Projekt-CoPilot mit Vollkontextprüfung und Kompatibilitätsgarantie

### 💬 Discord.py
- Slash Commands & Cogs: `/remind`, `/join`, `/champion`
- Rollenprüfung via OAuth2: R3_MEMBER, R4_ADMIN, ADMIN_ROLE_IDS
- Webhook-System (Champion-Poster, Reminder)

### 🌍 i18n-System
- gettext mit .po/.mo Dateien
- Auto-Import von Flaggen & Übersetzungen
- Multilingual Reminder & Event-System

### 🖥️ Web-Frontend
- HTML5 mit Jinja2 Templates
- Custom Pages: `/events/<id>`, `/admin`, `/hall-of-fame`
- CSS (style.css), Flaggen-Support, QR-Poster-Popup

### 🛡️ Security
- Discord OAuth2 Login
- Keyfile-System (optional)
- Rollenbasierte Zugangskontrolle: R3/R4/ADMIN
- Prepared SQL Statements

### 🔁 CI/CD & DevOps
- GitHub Actions (Lint, Test, Deploy)
- Railway Auto-Deploy mit Secrets
- Pre-Commit Hook: Auto-Fix + Formatierung
- Error Reports (`fix_report.md`)

---

## 📊 2. Aktive Funktionsbereiche

- Champion-Autopilot (monatlich, Poster, Hall-of-Fame, Discord Push)
- Reminder-System (Trigger, Zeitsteuerung, DM, i18n)
- Event-Management (Join-System, Reminder-Flow)
- Discord-Login + Dashboard-Anbindung
- Daily 22 Uhr Log: Wissens- & Fortschrittsdokumentation

---

## 📁 3. GPT-Wissen & Spezialisierungen

- Python: asyncio, unittest, pathlib, json, re, os, math
- C++: Datenstrukturen, Substitution Ciphers, Fehleranalyse
- Markdown & YAML: Dokumentation, GitHub Actions, Logs
- GitHub API: Secrets-Management, Deploy-Trigger, PR-Automation
- API-Rekonstruktion: Reverse Engineering mobiler GGW-App
- Wirtschaftsinformatik: Marketingstrategie, Marktforschung, Statistik

---

## 🔐 4. Rollen & Zugriff

| Rolle        | Beschreibung                         | Zugriff                        |
|--------------|--------------------------------------|--------------------------------|
| R3_ROLE_IDS  | Mitglieder                           | Events, Join, Downloads        |
| R4_ROLE_IDS  | Admins                               | Adminpanel, Reminder-System    |
| ADMIN_ROLE_IDS | Owner/System-Superuser            | Vollzugriff                    |

---

## 🚀 5. Zielgruppe & Projektvision

- Plattform: Grand Gangster War (GGW)
- Zielgruppen: Clanführer, Offiziere, Admins, Entwickler
- Allianz: FUR (Server #28) – erster Early Access
- Zukunft: GGW API-Anbindung, Öffnung für alle Spieler
- Modus: FUR Marcel aktiviert – GPT agiert projektzentriert, loyal & strategisch

---
