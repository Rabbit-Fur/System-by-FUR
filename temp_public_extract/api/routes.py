import sqlite3
import logging
from flask import jsonify, request, current_app
from . import api_bp
from app import get_db  # Importiere DB Helper aus Haupt-App

log = logging.getLogger(__name__)

# === API Endpoint: Events abrufen ===


@api_bp.route('/events', methods=['GET'])
def get_events():
    """Gibt eine Liste aller Events zurück (optional filterbar)."""
    # Beispiel: Nur zukünftige Events?
    # filter_future = request.args.get('future', 'false').lower() == 'true'
    try:
        conn = get_db()
        # Query anpassen, falls Filter benötigt werden
        query = "SELECT id, title, description, event_time, role, recurrence FROM events ORDER BY event_time ASC"
        events = conn.execute(query).fetchall()
        # Konvertiere Rows zu Dictionaries für JSON
        events_list = [dict(row) for row in events]
        log.debug(f"API: Fetched {len(events_list)} events.")
        return jsonify(events_list), 200
    except sqlite3.Error as e:
        log.error(f"API Error fetching events: {e}", exc_info=True)
        return jsonify({"error": "Database error fetching events."}), 500
    except Exception as e:
        log.error(f"API Unexpected error fetching events: {e}", exc_info=True)
        return jsonify({"error": "Internal server error."}), 500

# === API Endpoint: Einzelnes Event abrufen ===


@api_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    """Gibt Details zu einem spezifischen Event zurück."""
    try:
        conn = get_db()
        event = conn.execute(
            "SELECT id, title, description, event_time, role, recurrence FROM events WHERE id = ?",
            (event_id,)
        ).fetchone()
        if event is None:
            log.warning(f"API: Event ID {event_id} not found.")
            return jsonify(
                {"error": f"Event with ID {event_id} not found."}), 404
        log.debug(f"API: Fetched event ID {event_id}.")
        return jsonify(dict(event)), 200
    except sqlite3.Error as e:
        log.error(f"API Error fetching event {event_id}: {e}", exc_info=True)
        return jsonify({"error": "Database error fetching event."}), 500
    except Exception as e:
        log.error(
            f"API Unexpected error fetching event {event_id}: {e}",
            exc_info=True)
        return jsonify({"error": "Internal server error."}), 500

# === API Endpoint: Teilnehmer abrufen ===


@api_bp.route('/participants', methods=['GET'])
def get_participants():
    """Gibt eine Liste aller Teilnehmer zurück, optional gefiltert nach Event."""
    event_id_filter = request.args.get('event_id')
    try:
        conn = get_db()
        query = """
            SELECT p.id, p.event_id, p.username, p.joined_at, e.title AS event_title
            FROM participants p
            JOIN events e ON p.event_id = e.id
        """
        params = []
        if event_id_filter:
            try:
                params.append(int(event_id_filter))
                query += " WHERE p.event_id = ?"
            except ValueError:
                return jsonify({"error": "Invalid event_id parameter."}), 400

        query += " ORDER BY p.joined_at DESC"
        participants = conn.execute(query, params).fetchall()
        participants_list = [dict(row) for row in participants]
        log.debug(f"API: Fetched {len(participants_list)} participants.")
        return jsonify(participants_list), 200
    except sqlite3.Error as e:
        log.error(f"API Error fetching participants: {e}", exc_info=True)
        return jsonify({"error": "Database error fetching participants."}), 500
    except Exception as e:
        log.error(
            f"API Unexpected error fetching participants: {e}",
            exc_info=True)
        return jsonify({"error": "Internal server error."}), 500

# === API Endpoint: Hall of Fame abrufen ===


@api_bp.route('/hall_of_fame', methods=['GET'])
def get_hall_of_fame():
    """Gibt die Liste der Champions aus der Hall of Fame zurück."""
    try:
        conn = get_db()
        query = "SELECT id, username, honor_title, month, poster_url, created_at FROM hall_of_fame ORDER BY created_at DESC"
        champions = conn.execute(query).fetchall()
        champions_list = [dict(row) for row in champions]
        log.debug(
            f"API: Fetched {len(champions_list)} champions from Hall of Fame.")
        return jsonify(champions_list), 200
    except sqlite3.Error as e:
        log.error(f"API Error fetching Hall of Fame: {e}", exc_info=True)
        return jsonify({"error": "Database error fetching Hall of Fame."}), 500
    except Exception as e:
        log.error(
            f"API Unexpected error fetching Hall of Fame: {e}",
            exc_info=True)
        return jsonify({"error": "Internal server error."}), 500
