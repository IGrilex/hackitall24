import sqlite3

DB_NAME = 'hackitallDB.db'

def get_user_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id_user FROM User WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

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
        SELECT e.name, e.event_date, e.organizer, e.hours_of_work, e.location, COUNT(ue.id_user)
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
        'interested': row[5]
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