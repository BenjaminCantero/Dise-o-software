# proyecto_gestion_salas/database_setup.py
import sqlite3

DB_NAME = 'gestion_salas.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_tables(conn):
    """Creates all necessary tables in the database if they don't exist."""
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Crear tabla de salas (using the more complete definition)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            capacidad INTEGER NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Disponible' 
        )
    ''')
    
    # Crear tabla de reservas (using the more complete definition)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sala_id INTEGER NOT NULL,
            responsable TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_termino TEXT NOT NULL,
            motivo TEXT,
            estado TEXT NOT NULL DEFAULT 'Pendiente', 
            FOREIGN KEY (sala_id) REFERENCES salas(id)
        )
    ''')
    conn.commit()

def insert_default_users(conn):
    """Inserts default users if they don't already exist."""
    cursor = conn.cursor()
    users = [
        ('admin', 'admin123', 'admin'),
        ('profesor', 'profesor123', 'profesor'),
        ('estudiante', 'estudiante123', 'estudiante')
    ]
    
    for username, password, role in users:
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)", 
                           (username, password, role))
    conn.commit()

def initialize_database():
    """Connects to the DB, creates tables, and inserts default users."""
    conn = get_db_connection()
    create_tables(conn)
    insert_default_users(conn)
    # The connection is returned so the calling module can manage it or close it if it's only for initialization.
    # However, for LoginSistema and SistemaGestionSalas, they will each manage their own connection instance.
    conn.close()