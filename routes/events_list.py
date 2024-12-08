# routes/events_list.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models import get_all_active_events, get_event_tags, recommend_event, unrecommend_event
import sqlite3

events_list_bp = Blueprint('events_list', __name__, url_prefix='/events_list')

@events_list_bp.route('/', methods=['GET'])
def events_list():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view the events list.', 'error')
        return redirect(url_for('login.login'))
    return render_template('events_list.html')

@events_list_bp.route('/api/filter', methods=['GET'])
def filter_events():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # Get filter parameters
    keyword = request.args.get('keyword', '', type=str)
    month = request.args.get('month', type=int)
    order = request.args.get('order', 'date', type=str)  # 'date' or 'points'

    # Fetch all active events
    events = get_all_active_events(user_id)

    # Apply keyword filter
    if keyword:
        events = [event for event in events if keyword.lower() in event['name'].lower()]

    # Apply month filter
    if month:
        events = [event for event in events if event['date'].startswith(f"{month:02}")]

    # Apply ordering
    if order == 'date':
        events.sort(key=lambda x: x['date'])
    elif order == 'points':
        events.sort(key=lambda x: x['points'], reverse=True)

    return jsonify(events)

@events_list_bp.route('/recommend', methods=['POST'])
def recommend():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    event_id = data.get('event_id')
    action = data.get('action')

    if action == 'recommend':
        recommend_event(user_id, event_id)
    elif action == 'unrecommend':
        unrecommend_event(user_id, event_id)

    return jsonify({'status': 'success'})
