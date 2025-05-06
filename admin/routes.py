from flask_babel import _
import os
import time
import logging
from datetime import datetime, timedelta
from functools import wraps
from flask import (
    render_template, request, redirect, url_for, flash,
    session, current_app, abort
)
from werkzeug.utils import secure_filename
from . import admin_bp

logger = logging.getLogger(__name__)

# === AUTH & SESSION ===


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash(_('Please log in to access this area.'), 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.before_request
def check_session_timeout():
    if 'admin_logged_in' in session:
        last_active = session.get('admin_last_active')
        try:
            last_active_dt = datetime.strptime(
                last_active, "%Y-%m-%d %H:%M:%S.%f")
            timeout = current_app.config.get(
                'PERMANENT_SESSION_LIFETIME', timedelta(minutes=30))
            if datetime.utcnow() - last_active_dt > timeout:
                session.clear()
                flash(_('Session timed out due to inactivity.'), 'warning')
                return redirect(url_for('admin.login'))
        except Exception as e:
            logger.warning("Session timestamp error: %s", e)
            session.clear()
            flash(_('Session error. Please log in again.'), 'warning')
            return redirect(url_for('admin.login'))
        session['admin_last_active'] = datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S.%f")

# === FILE UPLOAD ===


def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    return '.' in filename and ext in current_app.config['ALLOWED_EXTENSIONS']

# === CHAMPION PLACEHOLDER ===


def assign_honor_title(username, target_month):
    return "🔥 Champion of the Month 🔥"


def determine_monthly_champion(target_month=None):
    # Placeholder-Logik
    pass

# === ROUTES ===


@admin_bp.route('/')
def admin_index():
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    username = session.get('admin_username', 'Admin')
    session.clear()
    flash(_('You have been logged out.'), 'success')
    logger.info(f"Admin '{username}' logged out.")
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@admin_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    return render_template('create_event.html')


@admin_bp.route('/events/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    return render_template('edit_event.html', event={})


@admin_bp.route('/events/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/events/<int:event_id>/participants')
@login_required
def view_participants(event_id):
    return render_template('participants.html', event={}, participants=[])


@admin_bp.route('/events/<int:event_id>/join', methods=['POST'])
@login_required
def join_event(event_id):
    return redirect(
        request.referrer or url_for(
            'public.view_event',
            event_id=event_id))


@admin_bp.route('/events/<int:event_id>/leave', methods=['POST'])
@login_required
def leave_event(event_id):
    return redirect(
        request.referrer or url_for(
            'public.view_event',
            event_id=event_id))


@admin_bp.route('/diplomacy')
@login_required
def diplomacy():
    return render_template('diplomacy.html')


@admin_bp.route('/downloads')
@login_required
def downloads():
    return render_template('downloads.html')


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@admin_bp.route('/translations')
@login_required
def translations_editor():
    return render_template('translations_editor.html')


@admin_bp.route('/tools')
@login_required
def tools():
    return render_template('tools.html')


@admin_bp.route('/trigger_champion')
@login_required
def trigger_champion_manually():
    try:
        month = request.args.get('month', datetime.utcnow().strftime('%Y-%m'))
        determine_monthly_champion(month)
        flash(f'Champion calculation for {month} triggered.', 'info')
    except Exception as e:
        flash(f'Champion error: {e}', 'danger')
        logger.error("Champion trigger failed", exc_info=True)
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    file = request.files.get('file')
    if not file or file.filename == '':
        flash(_('No file selected.'), 'warning')
        return redirect(request.referrer or url_for('admin.dashboard'))

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        final_name = f"{timestamp}_{filename}"
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        try:
            file.save(os.path.join(upload_folder, final_name))
            logger.info(f"File uploaded: {final_name}")
            flash(_('Upload successful: %(filename)s',
                  filename=final_name), 'success')
        except Exception as e:
            logger.error("Upload failed", exc_info=True)
            flash(_('File upload failed.'), 'error')
    else:
        flash(_('Invalid file type or size.'), 'error')

    return redirect(request.referrer or url_for('admin.dashboard'))
