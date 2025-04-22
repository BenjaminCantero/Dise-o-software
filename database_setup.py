import sqlite3

class DatabaseSetup:
    def __init__(self, db_name="gestion_salas.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def crear_tablas(self):
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
            motivo TEXT,
            FOREIGN KEY (sala_id) REFERENCES salas (id)
        )
        ''')

        # Crear tabla de usuarios
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')

    def insertar_usuarios_predeterminados(self):
        # Insertar usuarios predeterminados si no existen
        self.cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO usuarios (username, password, role) VALUES ('admin', 'admin123', 'admin')")
            self.cursor.execute("INSERT INTO usuarios (username, password, role) VALUES ('user', 'user123', 'user')")

    def obtener_usuario(self, username, password):
        # Buscar usuario por nombre de usuario y contraseña
        self.cursor.execute("SELECT role FROM usuarios WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone()

    def obtener_salas(self):
        # Obtener todas las salas
        self.cursor.execute("SELECT * FROM salas")
        return self.cursor.fetchall()

    def obtener_reservas(self):
        # Obtener todas las reservas
        self.cursor.execute("SELECT * FROM reservas")
        return self.cursor.fetchall()

    def inicializar_base_datos(self):
        self.crear_tablas()
        self.insertar_usuarios_predeterminados()
        self.conn.commit()

    def cerrar_conexion(self):
        self.conn.close()


if __name__ == "__main__":
    db_setup = DatabaseSetup()
    db_setup.inicializar_base_datos()
    db_setup.cerrar_conexion()