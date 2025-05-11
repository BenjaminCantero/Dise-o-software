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
        
        self.conn.commit()
    
    def obtener_usuario(self, username, password):
        """Obtiene el rol del usuario si las credenciales son válidas"""
        self.cursor.execute(
            "SELECT role FROM usuarios WHERE username = ? AND password = ?",
            (username, password)
        )
        return self.cursor.fetchone()
    
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