import math
import sqlite3

DB_NAME = 'hackitallDB.db'

def get_user_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id_user FROM User WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return {'id_user': user[0]} if user else None

def create_user(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO User (first_name, last_name, date_of_birth, gender, email, university, 
                          university_specialization, university_programme, employed_status, bio, hobbies)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['first_name'], data['last_name'], data['date_of_birth'], data['gender'],
        data['email'], data['university'], data['university_specialization'],
        data['university_programme'], data['employed_status'], data['bio'], data['hobbies']
    ))
    conn.commit()
    conn.close()

def get_events_by_month(month, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        SELECT e.id_event, e.name, e.description, e.event_date, e.location, e.openslots,
               CASE WHEN rl.id_event IS NULL THEN 0 ELSE 1 END AS recommended
        FROM Event e
        LEFT JOIN Recommendations_List rl 
            ON e.id_event = rl.id_event AND rl.id_user = ?
        WHERE strftime('%m', e.event_date) = ?
          AND e.status = 'active'
    """
    cursor.execute(query, (user_id, f"{month:02}",))
    events = cursor.fetchall()
    conn.close()

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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        SELECT e.id_event, e.name, e.description, e.event_date, e.location, e.openslots,
               CASE WHEN rl.id_event IS NULL THEN 0 ELSE 1 END AS recommended
        FROM Event e
        LEFT JOIN Recommendations_List rl 
            ON e.id_event = rl.id_event AND rl.id_user = ?
        WHERE e.status = 'active'
    """
    cursor.execute(query, (user_id,))
    events = cursor.fetchall()
    conn.close()

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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        SELECT t.name
        FROM Tag t
        JOIN Event_Tags et ON t.id_tag = et.id_tag
        WHERE et.id_event = ?
    """
    cursor.execute(query, (event_id,))
    tags = cursor.fetchall()
    conn.close()
    return [tag[0] for tag in tags]

def get_event_details(event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        SELECT e.name, e.event_date, e.organizer, e.hours_of_work, COUNT(ue.id_user)
        FROM Event e
        LEFT JOIN User_Events ue ON e.id_event = ue.id_event
        WHERE e.id_event = ?
        GROUP BY e.id_event
    """
    cursor.execute(query, (event_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        'name': row[0],
        'date': row[1],
        'organizer': row[2],
        'points': row[3] * 10,
        'interested': row[4]
    }

def get_event_location(event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT location FROM Event WHERE id_event = ?"
    cursor.execute(query, (event_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return row[0]

def is_user_enrolled(user_id, event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        SELECT 1 FROM User_Events
        WHERE id_user = ? AND id_event = ?
    """
    cursor.execute(query, (user_id, event_id))
    result = cursor.fetchone()
    conn.close()
    return bool(result)

def enroll_user_in_event(user_id, event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "INSERT INTO User_Events (id_user, id_event) VALUES (?, ?)"
    cursor.execute(query, (user_id, event_id))
    conn.commit()
    conn.close()

def remove_user_from_event(user_id, event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "DELETE FROM User_Events WHERE id_user = ? AND id_event = ?"
    cursor.execute(query, (user_id, event_id))
    conn.commit()
    conn.close()

def get_event_forums(event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        SELECT id_forum, name
        FROM Forum
        WHERE id_event = ?
    """
    cursor.execute(query, (event_id,))
    forums = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'name': row[1]} for row in forums]

def recommend_event(user_id, event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Recommendations_List (id_user, id_event) VALUES (?, ?)", (user_id, event_id))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Recommendation already exists
    finally:
        conn.close()

def unrecommend_event(user_id, event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Recommendations_List WHERE id_user = ? AND id_event = ?", (user_id, event_id))
    conn.commit()
    conn.close()
    
def get_user_details(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        SELECT first_name, last_name, date_of_birth, gender, email, university, 
               university_specialization, university_programme, employed_status, bio, hobbies
        FROM User
        WHERE id_user = ?
    """
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    conn.close()
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
    conn = sqlite3.connect(DB_NAME)
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
    conn.close()
    return row[0] if row[0] else 0

def get_available_points(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT points FROM User WHERE id_user = ?"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def get_total_points(user_id):
    # Total points are only from User_Events (calculated points)
    return get_user_events_points(user_id)

def get_user_level(points):
    if points < 100:
        return 1
    else:
        return int(math.log10(points))

def get_leaderboard(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Calculate total points for all users based on User_Events for inactive events
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
    conn.close()
    
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