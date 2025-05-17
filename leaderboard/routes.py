import logging
import sqlite3

from flask import Blueprint, jsonify, request

from app import get_db

log = logging.getLogger(__name__)
api_bp = Blueprint("api_leaderboard", __name__)


@api_bp.route("/error")
def error():
    return jsonify({"error": "Event not found"}), 404


@api_bp.route("/hall_of_fame", methods=["GET"])
def get_hall_of_fame_api():
    """Gibt die Liste der Champions aus der Hall of Fame zurück."""
    try:
        db = get_db()
        champions = db.execute(
            "SELECT username, honor_title, month, poster_url, created_at FROM hall_of_fame ORDER BY created_at DESC"
        ).fetchall()
        return jsonify([dict(row) for row in champions]), 200
    except sqlite3.Error as e:
        log.error(f"API Error fetching Hall of Fame: {e}", exc_info=True)
        return jsonify({"error": "Database error fetching Hall of Fame"}), 500
    except Exception as e:
        log.error(f"Unexpected API error fetching Hall of Fame: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/leaderboard/<category>", methods=["GET"])
def get_leaderboard_category(category):
    """Gibt Leaderboard-Scores für eine spezifische Kategorie zurück."""
    allowed_categories = {"raids", "quests", "donations", "building"}
    if category not in allowed_categories:
        return jsonify({"error": "Invalid category"}), 400

    period_filter = request.args.get("period", "alltime")

    query = """
        SELECT user_id, username, score
        FROM scores
        WHERE category = ? AND period = ?
        ORDER BY score DESC
        LIMIT 10
    """
    try:
        db = get_db()
        scores = db.execute(query, (category, period_filter)).fetchall()
        return jsonify([dict(row) for row in scores]), 200
    except sqlite3.Error as e:
        log.error(f"API Error fetching leaderboard for {category}: {e}", exc_info=True)
        return jsonify({"error": "Database error fetching leaderboard"}), 500
    except Exception as e:
        log.error(f"Unexpected API error fetching leaderboard for {category}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
