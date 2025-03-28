from database import connect_db

def get_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    conn.close()
    return rooms

def add_room(name, capacity, type):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rooms (name, capacity, type) VALUES (?, ?, ?)", 
                   (name, capacity, type))
    conn.commit()
    conn.close()
