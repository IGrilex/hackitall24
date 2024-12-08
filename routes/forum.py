# routes/forum.py
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models import get_posts_by_forum, get_forum_details, get_event_details, DB_NAME
import sqlite3

forum_bp = Blueprint('forum', __name__, url_prefix='/home/forum')

@forum_bp.route('/<int:forum_id>', methods=['GET', 'POST'])
def forum_page(forum_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view forums.', 'error')
        return redirect(url_for('login.login'))
    
    # Fetch forum details
    forum = get_forum_details(forum_id)
    if not forum:
        flash('Forum not found.', 'error')
        return redirect(url_for('home.home'))
    
    # Fetch event details
    event = get_event_details(forum['id_event'])
    if not event:
        flash('Associated event not found.', 'error')
        return redirect(url_for('home.home'))
    
    if request.method == 'POST':
        post_text = request.form.get('post_text')
        if not post_text or post_text.strip() == '':
            flash('Post cannot be empty.', 'error')
            return redirect(url_for('forum.forum_page', forum_id=forum_id))
        
        # Insert the new post into the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        query = """
            INSERT INTO Post (id_forum, id_user, text)
            VALUES (?, ?, ?)
        """
        cursor.execute(query, (forum_id, user_id, post_text.strip()))
        conn.commit()
        conn.close()
        
        flash('Post added successfully!', 'success')
        return redirect(url_for('forum.forum_page', forum_id=forum_id))
    
    # Fetch posts for the forum
    posts = get_posts_by_forum(forum_id)
    
    return render_template(
        'forum.html',
        event_title=event['name'],
        forum_title=forum['name'],
        posts=posts,
        forum_id=forum_id  # Ensure forum_id is passed to the template
    )
