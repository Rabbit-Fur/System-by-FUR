import sqlite3
import logging
from datetime import datetime
from flask import render_template, redirect, url_for, abort
from . import public_bp
from app import get_db

log = logging.getLogger(__name__)

# === Public Landing Page ===


@public_bp.route('/')
def landing():
    """Öffentliche Startseite."""
    # TODO: Optional Events oder News anzeigen
    return render_template('landing.html')

# === Hall of Fame ===


@public_bp.route('/hall-of-fame')
def hall_of_fame():
    """Zeigt die Champions der FUR Allianz."""
    try:
        with get_db() as conn:
            champions = conn.execute("""
                SELECT username, honor_title, month, poster_url
                FROM hall_of_fame
                ORDER BY created_at DESC
            """).fetchall()
        log.debug(f"HOF geladen: {len(champions)} Einträge.")
        return render_template('hall_of_fame.html', champions=champions)
    except sqlite3.Error as e:
        log.error("DB-Fehler in Hall of Fame: %s", e, exc_info=True)
        abort(500)
    except Exception as e:
        log.error("Unbekannter Fehler in Hall of Fame: %s", e, exc_info=True)
        abort(500)

# === Öffentliche Eventliste ===


@public_bp.route('/events')
def events_list():
    """Zeigt alle geplanten Events."""
    try:
        with get_db() as conn:
            events = conn.execute("""
                SELECT id, title, description, event_time, role, recurrence
                FROM events
                ORDER BY event_time ASC
            """).fetchall()
        log.debug(f"{len(events)} Events geladen.")
        return render_template(
            'events_list.html',
            events=events,
            now=datetime.utcnow())
    except sqlite3.Error as e:
        log.error("DB-Fehler beim Laden der Events: %s", e, exc_info=True)
        abort(500)
    except Exception as e:
        log.error(
            "Unbekannter Fehler beim Laden der Events: %s",
            e,
            exc_info=True)
        abort(500)

# === Einzelnes Event anzeigen ===


@public_bp.route('/events/<int:event_id>')
def view_event(event_id):
    """Öffentliche Ansicht eines Events + Teilnehmerliste."""
    try:
        with get_db() as conn:
            event = conn.execute("""
                SELECT id, title, description, event_time, role, recurrence
                FROM events
                WHERE id = ?
            """, (event_id,)).fetchone()

            if not event:
                abort(404)

            participants = conn.execute("""
                SELECT username FROM participants
                WHERE event_id = ?
            """, (event_id,)).fetchall()

        log.debug(f"Event-ID {event_id} geladen.")
        return render_template(
            "view_event.html",
            event=event,
            participants=participants)

    except sqlite3.Error as e:
        log.error(f"DB-Fehler bei Event {event_id}: %s", e, exc_info=True)
        abort(500)
    except Exception as e:
        log.error(
            f"Allgemeiner Fehler bei Event {event_id}: %s",
            e,
            exc_info=True)
        abort(500)

# === Lore Page (Optional) ===


@public_bp.route('/lore')
def lore_page():
    """Hintergrundgeschichte der FUR Allianz."""
    return render_template('lore.html')
