from flask import Blueprint, render_template, session, redirect, url_for, flash

public_bp = Blueprint('public', __name__, template_folder='templates')


@public_bp.route('/')
def landing():
    return render_template('public/landing.html')


@public_bp.route('/login')
def login():
    return render_template('public/login.html')


@public_bp.route('/calendar')
def calendar():
    return render_template('public/calendar.html')


@public_bp.route('/events_list')
def events_list():
    return render_template('public/events_list.html')


@public_bp.route('/hall_of_fame')
def hall_of_fame():
    return render_template('public/hall_of_fame.html')


@public_bp.route('/lore')
def lore():
    return render_template('public/lore.html')


@public_bp.route('/public_leaderboard')
def public_leaderboard():
    return render_template('public/public_leaderboard.html')


@public_bp.route('/view_event')
def view_event():
    return render_template('public/view_event.html')
