# app/db.py
from flask import g
import sqlite3  # Oder psycopg2, je nach deiner DB

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("your_database.db")  # Pfad ggf. anpassen
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
