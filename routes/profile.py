# routes/profile.py

from flask import Blueprint, render_template, session, redirect, url_for, flash, send_file
from models import (
    get_user_details,
    get_user_events_points,
    get_available_points,
    get_total_points,
    get_user_level,
    get_leaderboard
)
from utils.generate_certificate import create_certificate  # Import the certificate generation function
from io import BytesIO
from datetime import datetime

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('login.login'))
    
    user = get_user_details(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('home.home'))
    
    # Get points from inactive events (calculated points)
    calculated_points = get_user_events_points(user_id)
    
    # Get available points from User table
    available_points = get_available_points(user_id)
    
    # Total points are only the calculated points
    total_points = calculated_points
    
    # Calculate level based on total points
    level = get_user_level(total_points)
    
    # Get leaderboard based on total points
    leaderboard = get_leaderboard(user_id)
    
    return render_template(
        'profile.html',
        user=user,
        calculated_points=calculated_points,
        available_points=available_points,
        total_points=total_points,
        level=level,
        leaderboard=leaderboard
    )

@profile_bp.route('/certificate')
def download_certificate():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to download your certificate.', 'error')
        return redirect(url_for('login.login'))
    
    user = get_user_details(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('home.home'))
    
    # Get calculated points and level
    calculated_points = get_user_events_points(user_id)
    level = get_user_level(calculated_points)
    
    # Current date for the certificate
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Create the PDF certificate
    pdf_buffer = create_certificate(user['first_name'], user['last_name'], level, current_date)
    
    # Define the PDF filename
    filename = f"certificate_{user['first_name']}_{user['last_name']}.pdf"
    
    # Send the PDF as a downloadable file
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )
