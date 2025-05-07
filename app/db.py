from flask 
import gimport sqlite3  # oder deine DB
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("your_database.db")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
