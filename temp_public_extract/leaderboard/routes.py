import sqlite3
import logging
from flask import render_template, current_app, abort
from . import leaderboard_bp
from app import get_db  # Importiere DB Helper aus Haupt-App

log = logging.getLogger(__name__)


@leaderboard_bp.route('/')  # Route ist jetzt /leaderboard/
def show_leaderboards():
    """Zeigt die Leaderboard-Übersichtsseite an."""
    categories = [
        'raids',
        'quests',
        'donations',
        'building']  # Beispiel-Kategorien
    leaderboard_data = {}
    try:
        with get_db() as conn:
            for category in categories:
                # Hole Top 10 für jede Kategorie (Annahme: Tabelle 'scores'
                # existiert)
                query = """
                    SELECT s.user_id, u.username, s.score
                    FROM scores s
                    JOIN users u ON s.user_id = u.user_id
                    WHERE s.category = ? AND s.period = 'alltime' -- Beispiel: Allzeit-Ranking
                    ORDER BY s.score DESC
                    LIMIT 10
                """
                # Stelle sicher, dass die 'scores' Tabelle existiert und Daten
                # hat
                try:
                    leaderboard_data[category] = conn.execute(
                        query, (category,)).fetchall()
                except sqlite3.OperationalError as oe:
                    log.warning(
                        f"Leaderboard table 'scores' might be missing or query error: {oe}")
                    leaderboard_data[category] = []  # Leere Liste bei Fehler

        log.debug("Leaderboard data fetched successfully.")
        return render_template(
            'leaderboards.html',
            leaderboards=leaderboard_data,
            categories=categories)

    except sqlite3.Error as e:
        log.error(f"Database error fetching leaderboards: {e}", exc_info=True)
        abort(500)  # Interner Serverfehler
    except Exception as e:
        log.error(
            f"Unexpected error fetching leaderboards: {e}",
            exc_info=True)
        abort(500)
