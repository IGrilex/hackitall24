# routes/login.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import get_user_by_email

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        user = get_user_by_email(email)
        if user:
            session['user_id'] = user[0]  # Assuming id_user is the first column
            return redirect(url_for('home.home'))
        else:
            flash('Error: Email not found!', 'error')
    return render_template('login.html')
