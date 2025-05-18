from flask import Blueprint, render_template

landing_bp = Blueprint("landing_bp", __name__)

@landing_bp.route("/")
def landing_page():
    return render_template("landing.html")
