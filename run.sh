#!/bin/bash
echo "🚀 Starte FUR SYSTEM"
export FLASK_APP=main.py
export FLASK_ENV=production
flask run --host=0.0.0.0 --port=8080