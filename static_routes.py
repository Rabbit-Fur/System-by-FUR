from flask import Blueprint, render_template

static_bp = Blueprint("static_bp", __name__)
@static_bp.route("/admin/admin")
def admin():
    return render_template("admin/admin.html")

@static_bp.route("/base")
def base():
    return render_template("base.html")

@static_bp.route("/admin/calendar")
def calendar():
    return render_template("admin/calendar.html")

@static_bp.route("/calendar")
def calendar():
    return render_template("calendar.html")

@static_bp.route("/admin/create_event")
def create_event():
    return render_template("admin/create_event.html")

@static_bp.route("/admin/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

@static_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@static_bp.route("/admin/diplomacy")
def diplomacy():
    return render_template("admin/diplomacy.html")

@static_bp.route("/admin/downloads")
def downloads():
    return render_template("admin/downloads.html")

@static_bp.route("/admin/edit_event")
def edit_event():
    return render_template("admin/edit_event.html")

@static_bp.route("/error")
def error():
    return render_template("error.html")

@static_bp.route("/admin/events")
def events():
    return render_template("admin/events.html")

@static_bp.route("/events_list")
def events_list():
    return render_template("events_list.html")

@static_bp.route("/hall_of_fame")
def hall_of_fame():
    return render_template("hall_of_fame.html")

@static_bp.route("/landing")
def landing():
    return render_template("landing.html")

@static_bp.route("/layout")
def layout():
    return render_template("layout.html")

@static_bp.route("/admin/leaderboards")
def leaderboards():
    return render_template("admin/leaderboards.html")

@static_bp.route("/leaderboards")
def leaderboards():
    return render_template("leaderboard/leaderboards.html")

@static_bp.route("/login")
def login():
    return render_template("login.html")

@static_bp.route("/lore")
def lore():
    return render_template("lore.html")

@static_bp.route("/member_dashboard")
def member_dashboard():
    return render_template("members/member_dashboard.html")

@static_bp.route("/member_downloads")
def member_downloads():
    return render_template("members/member_downloads.html")

@static_bp.route("/member_stats")
def member_stats():
    return render_template("members/member_stats.html")

@static_bp.route("/admin/participants")
def participants():
    return render_template("admin/participants.html")

@static_bp.route("/public_leaderboard")
def public_leaderboard():
    return render_template("public/public_leaderboard.html")

@static_bp.route("/admin/settings")
def settings():
    return render_template("admin/settings.html")

@static_bp.route("/settings")
def settings():
    return render_template("members/settings.html")

@static_bp.route("/admin/tools")
def tools():
    return render_template("admin/tools.html")

@static_bp.route("/admin/translations_editor")
def translations_editor():
    return render_template("admin/translations_editor.html")

@static_bp.route("/view_event")
def view_event():
    return render_template("public/view_event.html")
