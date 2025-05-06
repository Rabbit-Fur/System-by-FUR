# 🐰 GGWbyFUR Command Center

Modulares Flask-Dashboard mit Discord-Bot-Integration  
Für Events, Leaderboards, Member-Login & automatische Reminder

## 📦 Features
- Flask + Gunicorn-basiertes Admin-Panel
- Discord-Bot mit Cogs (Reminder, Leaderboard, Events)
- SQLite/PostgreSQL kompatibel
- APScheduler Reminder-System
- i18n JSON-basiert
- Railway-Ready Deployment

## 🚀 Deployment
- via [Railway](https://railway.app)
- `Procfile` für Gunicorn-Webserver
- `.env` mit Secrets & Tokens

## ⚙️ Struktur
- `app.py` / `wsgi.py` → Flask App
- `run.py` → Bot + Webserver kombi
- `bot/` → Cogs (Reminder etc.)
- `templates/` → Jinja2 HTML Templates
- `translations/` → JSON Sprachdateien


<!-- CI trigger: 2025-05-04T18:27:57.003363Z -->

<!-- CI retrigger: 2025-05-04T19:12:30.714327 -->

<!-- CI retrigger: 2025-05-04T19:34:10.354072 -->
