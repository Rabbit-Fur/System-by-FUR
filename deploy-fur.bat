@echo off
SETLOCAL ENABLEEXTENSIONS

cd /d "%~dp0"

echo Initialisiere Git...
git init
git remote remove origin >nul 2>&1
git remote add origin https://github.com/Rabbit-Fur/System-by-FUR.git

echo Erstelle .gitignore...
echo .env> .gitignore

echo Alle Dateien hinzufügen...
git add .

echo Commit ausführen...
git commit -m "Initial full project upload with Railway and .env"

echo Force Push nach GitHub...
git branch -M main
git push -u origin main --force

echo Railway Login (manuell falls nötig)...
railway login

echo Railway-Projekt initialisieren...
railway init

echo Importiere .env in Railway...
railway variables import .env

echo ✅ Deployment abgeschlossen!
pause
