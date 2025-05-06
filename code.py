import logging
log = logging.getLogger(__name__)
# --- START OF FILE leaderboard/__init__.py ---

leaderboard_bpreturn jsonify({"error": "Event not found"}), 404

# TODO: Sicherstellen, dass `db` definiert ist
        participants = db.execute(
            "SELECT username, joined_at, checked_in FROM participants WHERE event_id = ? ORDER BY joined_at ASC",
            (event_id,)
        ).fetchall()
        return jsonify([dict(row) for row in participants]), 200
    except sqlite3.Error as e:
# TODO: Sicherstellen, dass `log` definiert ist
        log.error(f"API Error fetching participants for event {event_id}: {e}", exc_info=True)
        return jsonify({"error": "Database error fetching participants"}), 500
    except Exception as e:
# TODO: Sicherstellen, dass `log` definiert ist
        log.error(f"Unexpected API error fetching participants for event {event_id}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# === API Endpoint: Hall of Fame abrufen ===
@api_bp.route('/hall_of_fame', methods=['GET'])
def get_hall_of_fame_api():
    """Gibt die Liste der Champions aus der Hall of Fame zurück."""
    try:
        db = get_db()
        champions = db.execute(
            "SELECT username, honor_title, month, poster_url, created_at FROM hall_of_fame ORDER BY created_at DESC"
        ).fetchall()
        return jsonify([dict(row) for row in champions]), 200
    except sqlite3.Error as e:
# TODO: Sicherstellen, dass `log` definiert ist
        log.error(f"API Error fetching Hall of Fame: {e}", exc_info=True)
        return jsonify({"error": "Database error fetching Hall of Fame"}), 500
    except Exception as e:
# TODO: Sicherstellen, dass `log` definiert ist
        log.error(f"Unexpected API error fetching Hall of Fame: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# === Optional: API Endpoint für Leaderboard Scores ===
@api_bp.route('/leaderboard/<category>', methods=['GET'])
def get_leaderboard_category(category):
    """Gibt Leaderboard-Scores für eine spezifische Kategorie zurück."""
    allowed_categories = {'raids', 'quests', 'donations', 'building'} # Beispiel
    if category not in allowed_categories:
        return jsonify({"error": "Invalid category"}), 400

    # Optional: Filter nach Periode (z.B. ?period=weekly_2024_15)
    period_filter = request.args.get('period', 'alltime') # Default: Allzeit

    query = """
        SELECT user_id, username, score
        FROM scores
        WHERE category = ? AND period = ?
        ORDER BY score DESC
        LIMIT 10
    """
    params = (category, period_filter)

    try:
        db = get_db()
        # Join mit users Tabelle, um Usernamen zu holen (falls user_id gespeichert ist)
        # Passe Query an, falls scores.username direkt gespeichert wird
        scores = db.execute(query, params).fetchall()
        return jsonify([dict(row) for row in scores]), 200
    except sqlite3.Error as e:
# TODO: Sicherstellen, dass `log` definiert ist
        log.error(f"API Error fetching leaderboard for {category}: {e}", exc_info=True)
        return jsonify({"error": "Database error fetching leaderboard"}), 500
    except Exception as e:
# TODO: Sicherstellen, dass `log` definiert ist
        log.error(f"Unexpected API error fetching leaderboard for {category}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


# --- END OF FILE api/routes.py ---