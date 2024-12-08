import math
import sqlite3

DB_NAME = 'hackitallDB.db'

def get_user_by_email(email):
    """
    Retrieves a user by their email address.
    Returns a dictionary with 'id_user' if found, else None.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = "SELECT id_user FROM User WHERE email = ?"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
    
    return {'id_user': user[0]} if user else None

def create_user(data):
    """
    Creates a new user in the User table.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO User (
                first_name, last_name, date_of_birth, gender, email, university, 
                university_specialization, university_programme, employed_status, bio, hobbies
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            data['first_name'], data['last_name'], data['date_of_birth'], data['gender'],
            data['email'], data['university'], data['university_specialization'],
            data['university_programme'], data['employed_status'], data['bio'], data['hobbies']
        ))
        # No need to call conn.commit() as the context manager commits automatically on success

def get_events_by_month(month, user_id):
    """
    Retrieves events for a specific month and user.
    Includes event tags and recommendation status.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                e.id_event, e.name, e.description, e.event_date, e.location, e.openslots,
                CASE WHEN rl.id_event IS NULL THEN 0 ELSE 1 END AS recommended
            FROM Event e
            LEFT JOIN Recommendations_List rl 
                ON e.id_event = rl.id_event AND rl.id_user = ?
            WHERE strftime('%m', e.event_date) = ?
              AND e.status = 'active'
        """
        cursor.execute(query, (user_id, f"{month:02}",))
        events = cursor.fetchall()
    
    # Include tags for each event
    return [
        {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'location': row[4],
            'openslots': row[5],
            'tags': get_event_tags(row[0]),
            'recommended': bool(row[6])
        }
        for row in events
    ]

def get_all_active_events(user_id):
    """
    Retrieves all active events for a user.
    Includes event tags and recommendation status.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                e.id_event, e.name, e.description, e.event_date, e.location, e.openslots,
                CASE WHEN rl.id_event IS NULL THEN 0 ELSE 1 END AS recommended
            FROM Event e
            LEFT JOIN Recommendations_List rl 
                ON e.id_event = rl.id_event AND rl.id_user = ?
            WHERE e.status = 'active'
        """
        cursor.execute(query, (user_id,))
        events = cursor.fetchall()
    
    # Include tags for each event
    return [
        {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'date': row[3],
            'location': row[4],
            'openslots': row[5],
            'tags': get_event_tags(row[0]),
            'recommended': bool(row[6])
        }
        for row in events
    ]

def get_event_tags(event_id):
    """
    Retrieves all tags associated with a specific event.
    Returns a list of tag names.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT t.name
            FROM Tag t
            JOIN Event_Tags et ON t.id_tag = et.id_tag
            WHERE et.id_event = ?
        """
        cursor.execute(query, (event_id,))
        tags = cursor.fetchall()
    
    return [tag[0] for tag in tags]

def get_event_location(event_id):
    """
    Retrieves the location of a specific event.
    Returns the location as a string, or None if not found.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = "SELECT location FROM Event WHERE id_event = ?"
        cursor.execute(query, (event_id,))
        row = cursor.fetchone()
    
    return row[0] if row else None

def is_user_enrolled(user_id, event_id):
    """
    Checks if a user is enrolled in a specific event.
    Returns True if enrolled, False otherwise.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT 1 FROM User_Events
            WHERE id_user = ? AND id_event = ?
        """
        cursor.execute(query, (user_id, event_id))
        result = cursor.fetchone()
    
    return bool(result)

def enroll_user_in_event(user_id, event_id):
    """
    Enrolls a user in a specific event.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = "INSERT INTO User_Events (id_user, id_event) VALUES (?, ?)"
        cursor.execute(query, (user_id, event_id))
        # Context manager commits automatically

def remove_user_from_event(user_id, event_id):
    """
    Removes a user's enrollment from a specific event.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = "DELETE FROM User_Events WHERE id_user = ? AND id_event = ?"
        cursor.execute(query, (user_id, event_id))
        # Context manager commits automatically

def get_event_forums(event_id):
    """
    Retrieves all forums associated with a specific event.
    Returns a list of dictionaries with 'id' and 'name' keys.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT id_forum, name
            FROM Forum
            WHERE id_event = ?
        """
        cursor.execute(query, (event_id,))
        forums = cursor.fetchall()
    
    return [{'id': row[0], 'name': row[1]} for row in forums]

def recommend_event(user_id, event_id):
    """
    Adds a recommendation for a user to a specific event.
    Handles IntegrityError if the recommendation already exists.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        try:
            query = "INSERT INTO Recommendations_List (id_user, id_event) VALUES (?, ?)"
            cursor.execute(query, (user_id, event_id))
            # Context manager commits automatically
        except sqlite3.IntegrityError:
            pass  # Recommendation already exists

def unrecommend_event(user_id, event_id):
    """
    Removes a recommendation for a user from a specific event.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = "DELETE FROM Recommendations_List WHERE id_user = ? AND id_event = ?"
        cursor.execute(query, (user_id, event_id))
        # Context manager commits automatically

def get_user_details(user_id):
    """
    Retrieves detailed information about a user.
    Returns a dictionary with user details or None if not found.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT first_name, last_name, date_of_birth, gender, email, university, 
                   university_specialization, university_programme, employed_status, bio, hobbies
            FROM User
            WHERE id_user = ?
        """
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
    
    if not row:
        return None
    
    return {
        'first_name': row[0],
        'last_name': row[1],
        'date_of_birth': row[2],
        'gender': row[3],
        'email': row[4],
        'university': row[5],
        'university_specialization': row[6],
        'university_programme': row[7],
        'employed_status': row[8],
        'bio': row[9],
        'hobbies': row[10]
    }

def get_user_events_points(user_id):
    """
    Calculates the sum of points from inactive events for a user.
    Points are calculated as hours_of_work * 10.
    Returns the total points as an integer.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT SUM(e.hours_of_work * 10)
            FROM User_Events ue
            JOIN Event e ON ue.id_event = e.id_event
            WHERE ue.id_user = ?
              AND e.status = 'inactive'
        """
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
    
    return row[0] if row and row[0] else 0

def get_available_points(user_id):
    """
    Retrieves available points from the User table.
    Returns the points as an integer or 0 if not found.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = "SELECT points FROM User WHERE id_user = ?"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
    
    return row[0] if row else 0

def get_total_points(user_id):
    """
    Retrieves total points for a user.
    Currently, it returns the sum of points from inactive events.
    """
    return get_user_events_points(user_id)

def get_user_level(points):
    """
    Determines the user's level based on total points.
    Returns an integer representing the level.
    """
    if points < 100:
        return 1
    else:
        return int(math.log10(points))

def get_leaderboard(user_id):
    """
    Retrieves leaderboard data, highlighting the current user's position.
    Returns a dictionary with 'first_user', 'before_user', 'current_user', and 'after_user'.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT u.id_user, u.first_name, u.last_name, 
                   IFNULL(SUM(e.hours_of_work * 10), 0) AS total_points
            FROM User u
            LEFT JOIN User_Events ue ON u.id_user = ue.id_user
            LEFT JOIN Event e ON ue.id_event = e.id_event AND e.status = 'inactive'
            GROUP BY u.id_user
            ORDER BY total_points DESC, u.id_user ASC
        """
        cursor.execute(query)
        users = cursor.fetchall()
    
    # Create a sorted list of users by total points descending
    leaderboard = [
        {
            'id_user': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'total_points': row[3]
        }
        for row in users
    ]
    
    # Find the index of the current user
    current_user_index = next((i for i, u in enumerate(leaderboard) if u['id_user'] == user_id), None)
    
    if current_user_index is None:
        return {
            'first_user': None,
            'before_user': None,
            'current_user': None,
            'after_user': None
        }
    
    # Get first user
    first_user = leaderboard[0]
    
    # Get previous, current, next user
    before_user = leaderboard[current_user_index - 1] if current_user_index > 0 else None
    current_user = leaderboard[current_user_index]
    after_user = leaderboard[current_user_index + 1] if current_user_index < len(leaderboard) - 1 else None
    
    # Return first user and before/after users
    return {
        'first_user': first_user,
        'before_user': before_user,
        'current_user': current_user,
        'after_user': after_user
    }
        
def get_forums_by_event(event_id):
    """
    Retrieves all forums associated with a specific event, including the latest post date.
    Returns a list of dictionaries with 'id_forum', 'name', and 'last_update'.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT f.id_forum, f.name, MAX(p.date_of_post) AS last_update
            FROM Forum f
            LEFT JOIN Post p ON f.id_forum = p.id_forum
            WHERE f.id_event = ?
            GROUP BY f.id_forum, f.name
            ORDER BY last_update DESC
        """
        cursor.execute(query, (event_id,))
        forums = cursor.fetchall()
    
    # Format the result into a list of dictionaries
    return [
        {
            'id_forum': row[0],
            'name': row[1],
            'last_update': row[2] if row[2] else 'No posts yet'
        }
        for row in forums
    ]

def get_posts_by_forum(forum_id):
    """
    Retrieves all posts within a specific forum, ordered chronologically.
    Returns a list of dictionaries with post details.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT p.id_post, p.id_user, u.first_name, u.last_name, p.text, p.date_of_post
            FROM Post p
            JOIN User u ON p.id_user = u.id_user
            WHERE p.id_forum = ?
            ORDER BY p.date_of_post ASC
        """
        cursor.execute(query, (forum_id,))
        posts = cursor.fetchall()
    
    # Format the result
    return [
        {
            'id_post': row[0],
            'id_user': row[1],
            'first_name': row[2],
            'last_name': row[3],
            'text': row[4],
            'date_of_post': row[5]
        }
        for row in posts
    ]

def get_forum_details(forum_id):
    """
    Retrieves details of a specific forum.
    Returns a dictionary with 'id_forum', 'name', and 'id_event' or None if not found.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT id_forum, name, id_event
            FROM Forum
            WHERE id_forum = ?
        """
        cursor.execute(query, (forum_id,))
        row = cursor.fetchone()
    
    if not row:
        return None
    return {
        'id_forum': row[0],
        'name': row[1],
        'id_event': row[2]
    }

def get_event_details(event_id):
    """
    Retrieves details of a specific event.
    Returns a dictionary with 'id_event' and 'name' or None if not found.
    """
    with sqlite3.connect(DB_NAME, timeout=30) as conn:
        cursor = conn.cursor()
        query = """
            SELECT id_event, name
            FROM Event
            WHERE id_event = ?
        """
        cursor.execute(query, (event_id,))
        row = cursor.fetchone()
    
    if not row:
        return None
    return {
        'id_event': row[0],
        'name': row[1]
    }
