from flask import Blueprint, render_template, request, jsonify
from models import get_events_by_month

home_bp = Blueprint('home', __name__, url_prefix='/home')

@home_bp.route('/<int:user_id>')
def home(user_id):
    return render_template('map.html', user_id=user_id)

@home_bp.route('/events', methods=['GET'])
def get_events():
    month = request.args.get('month', type=int)
    events = get_events_by_month(month)
    return jsonify(events)
