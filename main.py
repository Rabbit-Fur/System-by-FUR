# main.py – FUR SYSTEM clean start
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "FUR SYSTEM ready."

if __name__ == "__main__":
    app.run(debug=True)