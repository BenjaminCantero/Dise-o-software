import sqlite3

class DatabaseSetup:
    def __init__(self, db_name='gestion_salas.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def inicializar_base_datos(self):
        """Inicializa la base de datos con las tablas necesarias"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        # Crear tabla de usuarios
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        # Crear tabla de salas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS salas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                capacidad INTEGER NOT NULL,
                estado TEXT NOT NULL
            )
        ''')
        # Crear tabla de reservas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sala_id INTEGER,
                responsable TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_termino TEXT NOT NULL,
                estado TEXT NOT NULL,
                FOREIGN KEY (sala_id) REFERENCES salas(id)
            )
        ''')
        
        # Insertar usuarios predeterminados
        self.cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
        if not self.cursor.fetchone():
            usuarios = [
                ('admin', 'admin123', 'admin'),
                ('profesor', 'profesor123', 'profesor'),
                ('estudiante', 'estudiante123', 'estudiante')
            ]
            self.cursor.executemany(
                "INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)",
                usuarios
            )
        # Insertar salas predeterminadas
        self.cursor.execute("SELECT * FROM salas")
        if not self.cursor.fetchone():
            salas = [
                ('Sala A', 20, 'Disponible'),
                ('Sala B', 15, 'Reservada'),
                ('Sala C', 30, 'Disponible')
            ]
            self.cursor.executemany(
                "INSERT INTO salas (nombre, capacidad, estado) VALUES (?, ?, ?)",
                salas
            )
        self.conn.commit()
    
    def obtener_usuario(self, username, password):
        """Obtiene el rol del usuario si las credenciales son válidas"""
        self.cursor.execute(
            "SELECT role FROM usuarios WHERE username = ? AND password = ?",
            (username, password)
        )
        return self.cursor.fetchone()
    
    def obtener_salas(self):
        """Devuelve todas las salas registradas en la base de datos"""
        self.cursor.execute("SELECT id, nombre, capacidad, estado FROM salas")
        return self.cursor.fetchall()
    
    def obtener_reservas(self, role=None, username=None):
        """
        Devuelve todas las reservas si es admin,
        o solo las del usuario si es profesor o estudiante.
        """
        if role == "admin" or role is None:
            self.cursor.execute("SELECT id, sala_id, responsable, fecha, hora_inicio, hora_termino, estado FROM reservas")
        else:
            self.cursor.execute(
                "SELECT id, sala_id, responsable, fecha, hora_inicio, hora_termino, estado FROM reservas WHERE responsable = ?",
                (username,)
            )
        return self.cursor.fetchall()
    
    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

if __name__ == "__main__":
    db = DatabaseSetup()
    db.inicializar_base_datos()
    db.cerrar_conexion()