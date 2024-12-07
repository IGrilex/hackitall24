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
        SELECT name, description, event_date, location 
        FROM Event 
        WHERE strftime('%m', event_date) = ?
          AND status = 'active'
    """
    cursor.execute(query, (f"{month:02}",))
    events = cursor.fetchall()
    conn.close()
    return [{'name': row[0], 'description': row[1], 'date': row[2], 'location': row[3]} for row in events]

