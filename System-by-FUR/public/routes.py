import logging
import sqlite3
from datetime import datetime

from flask import abort, render_template

import app

from . import public_bp

log = logging.getLogger(__name__)

# === Public Landing Page ===


@public_bp.route("/")
def landing():
    """Öffentliche Startseite."""
    return render_template("landing.html")


# === Hall of Fame ===


@public_bp.route("/hall-of-fame")
def hall_of_fame():
    """Zeigt die Champions der FUR Allianz."""
    try:
        conn = app.get_db()
        champions = conn.execute(
            """
            SELECT username, honor_title, month, poster_url
            FROM hall_of_fame
            ORDER BY created_at DESC
            """
        ).fetchall()
        return render_template("hall_of_fame.html", champions=champions)
    except sqlite3.Error as e:
        log.error(f"Error fetching hall_of_fame: {e}", exc_info=True)
        abort(500)


# === Öffentliche Eventansicht ===


@public_bp.route("/events/<int:event_id>")
def view_event(event_id):
    """Öffentliche Ansicht eines Events + Teilnehmerliste."""
    try:
        conn = app.get_db()

        event = conn.execute(
            """
            SELECT id, title, description, event_time, role, recurrence
            FROM events
            WHERE id = ?
            """,
            (event_id,),
        ).fetchone()

        if not event:
            abort(404)

        participants = conn.execute(
            """
            SELECT username
            FROM participants
            WHERE event_id = ?
            """,
            (event_id,),
        ).fetchall()

        return render_template("view_event.html", event=event, participants=participants)

    except sqlite3.Error as e:
        log.error(f"Error fetching event {event_id}: {e}", exc_info=True)
        abort(500)
