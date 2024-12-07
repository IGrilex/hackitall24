from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import create_user
import re
from datetime import datetime

signup_bp = Blueprint('signup', __name__, url_prefix='/signup')

@signup_bp.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract data from the form
        data = {
            'first_name': request.form.get('first_name', '').strip(),
            'last_name': request.form.get('last_name', '').strip(),
            'date_of_birth': request.form.get('date_of_birth', '').strip(),
            'gender': request.form.get('gender', '').strip(),
            'email': request.form.get('email', '').strip(),
            'university': request.form.get('university', '').strip(),
            'university_specialization': request.form.get('university_specialization', '').strip(),
            'university_programme': request.form.get('university_programme', '').strip(),
            'employed_status': request.form.get('employed_status', '').strip(),
            'bio': request.form.get('bio', '').strip(),
            'hobbies': request.form.get('hobbies', '').strip()
        }
        
        # Validation
        errors = []
        if not data['first_name']:
            errors.append("First name is required.")
        if not data['last_name']:
            errors.append("Last name is required.")
        if data['date_of_birth']:
            try:
                datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            except ValueError:
                errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
        if data['gender'] not in ['M', 'F', 'O']:
            errors.append("Invalid gender selected.")
        if not re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
            errors.append("Invalid email address.")
        if not data['university_specialization']:
            errors.append("Specialization is required.")
        if data['university_programme'] not in ['bachelor', 'master', 'phd']:
            errors.append("Invalid programme selected.")
        if data['employed_status'] not in ['Employed', 'Unemployed']:
            errors.append("Invalid employment status selected.")
        if data['hobbies'] and len(data['hobbies'].split(',')) > 10:
            errors.append("You can add up to 10 hobbies only.")
        
        # If there are validation errors, show them and re-render the form 
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('signup.html')
        
        # If no errors, save user to the database
        create_user(data)
        flash('User created successfully. Please log in!', 'success')
        return redirect(url_for('login.login'))
    
    return render_template('signup.html')
