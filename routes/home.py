# routes/home.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models import (
    get_events_by_month,
    get_event_details,
    get_event_location,
    get_forums_by_event,
    is_user_enrolled,
    enroll_user_in_event,
    remove_user_from_event,
    get_event_forums
)
import sqlite3

home_bp = Blueprint('home', __name__, url_prefix='/home')

@home_bp.route('/')
def home():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to access the home page.', 'error')
        return redirect(url_for('login.login'))
    return render_template('map.html', user_id=user_id)

@home_bp.route('/events', methods=['GET'])
def get_events():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    month = request.args.get('month', type=int)
    events = get_events_by_month(month, user_id)
    return jsonify(events)
     
@home_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_page(event_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view events.', 'error')
        return redirect(url_for('login.login'))
    
    event = get_event_details(event_id)
    if not event:
        flash('Event not found.', 'error')
        return redirect(url_for('home.home'))
    
    forums = get_forums_by_event(event_id)
    enrolled = is_user_enrolled(user_id, event_id)
    location = get_event_location(event_id)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'enroll' and not enrolled:
            try:
                enroll_user_in_event(user_id, event_id)
                enrolled = True
            except sqlite3.IntegrityError:
                flash('Error: Unable to enroll in the event.', 'error')
        elif action == 'leave' and enrolled:
            remove_user_from_event(user_id, event_id)
            enrolled = False
        return redirect(url_for('home.event_page', event_id=event_id))

    return render_template(
        'event.html',
        event=event,
        enrolled=enrolled,
        forums=forums,
        location=location
    )