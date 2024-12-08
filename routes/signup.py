# routes/signup.py
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import create_user

signup_bp = Blueprint('signup', __name__, url_prefix='/signup')

@signup_bp.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'date_of_birth': request.form['date_of_birth'],
            'gender': request.form['gender'],
            'email': request.form['email'],
            'university': request.form['university'],
            'university_specialization': request.form['university_specialization'],
            'university_programme': request.form['university_programme'],
            'employed_status': request.form['employed_status'],
            'bio': request.form['bio'],
            'hobbies': request.form['hobbies']
        }
        try:
            create_user(data)
            flash('User created successfully. Please log in!', 'success')
            return redirect(url_for('login.login'))
        except sqlite3.IntegrityError:
            flash('Error: Email already exists!', 'error')
    return render_template('signup.html')
