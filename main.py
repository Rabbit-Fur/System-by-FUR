import os
from dotenv import load_dotenv

load_dotenv()

from web import app
from bot import start_bot

if __name__ == "__main__":
    start_bot()
    app.run()
