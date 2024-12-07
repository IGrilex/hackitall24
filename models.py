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
    
def get_events_by_month(month):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        SELECT id_event, name, description, event_date, location, openslots
        FROM Event
        WHERE strftime('%m', event_date) = ?
          AND status = 'active'
    """
    cursor.execute(query, (f"{month:02}",))
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
            'tags': get_event_tags(row[0])
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

def get_event_by_id(event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = """
        SELECT id_event, name, event_date, openslots 
        FROM Event
        WHERE id_event = ?
    """
    cursor.execute(query, (event_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        'id': row[0],
        'name': row[1],
        'date': row[2],
        'openslots': row[3]
    }


