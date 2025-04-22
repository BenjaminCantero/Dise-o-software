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
            estado TEXT NOT NULL DEFAULT 'Pendiente',
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
            self.cursor.execute("INSERT INTO usuarios (username, password, role) VALUES ('profesor', 'profesor123', 'profesor')")
            self.cursor.execute("INSERT INTO usuarios (username, password, role) VALUES ('estudiante', 'estudiante123', 'estudiante')")

    def insertar_salas_predeterminadas(self):
        # Insertar salas predeterminadas si no existen
        self.cursor.execute("SELECT * FROM salas")
        if not self.cursor.fetchone():
            salas = [
                ("Sala A", 20, "Disponible"),
                ("Sala B", 15, "Reservada"),
                ("Sala C", 30, "Disponible"),
                ("Sala D", 25, "Reservada")
            ]
            self.cursor.executemany("INSERT INTO salas (nombre, capacidad, estado) VALUES (?, ?, ?)", salas)

    def insertar_reservas_predeterminadas(self):
        # Insertar reservas predeterminadas si no existen
        self.cursor.execute("SELECT * FROM reservas")
        if not self.cursor.fetchone():
            reservas = [
                (1, "Admin", "2025-04-21", "10:00", "12:00", "Reunión de equipo", "Confirmada"),
                (2, "Profesor", "2025-04-22", "14:00", "16:00", "Clase especial", "Pendiente")
            ]
            self.cursor.executemany(
                "INSERT INTO reservas (sala_id, responsable, fecha, hora_inicio, hora_termino, motivo, estado) VALUES (?, ?, ?, ?, ?, ?, ?)",
                reservas
            )

    def obtener_usuario(self, username, password):
        # Buscar usuario por nombre de usuario y contraseña
        self.cursor.execute("SELECT role FROM usuarios WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone()

    def obtener_salas(self):
        # Obtener todas las salas
        self.cursor.execute("SELECT id, nombre, capacidad, estado FROM salas")
        return self.cursor.fetchall()

    def obtener_reservas(self, role, username=None):
        if role == "admin":
            # El admin ve todas las reservas
            query = '''
            SELECT r.id, s.nombre AS sala, r.responsable, r.fecha, r.hora_inicio, r.hora_termino, r.estado
            FROM reservas r
            JOIN salas s ON r.sala_id = s.id
            '''
            self.cursor.execute(query)
        else:
            # Profesores y estudiantes solo ven sus reservas
            query = '''
            SELECT r.id, s.nombre AS sala, r.responsable, r.fecha, r.hora_inicio, r.hora_termino, r.estado
            FROM reservas r
            JOIN salas s ON r.sala_id = s.id
            WHERE r.responsable = ?
            '''
            self.cursor.execute(query, (username,))
        return self.cursor.fetchall()

    def insertar_reserva(self, sala_id, responsable, fecha, hora_inicio, hora_termino, estado):
        try:
            query = """
            INSERT INTO reservas (sala_id, responsable, fecha, hora_inicio, hora_termino, estado)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (sala_id, responsable, fecha, hora_inicio, hora_termino, estado))
            self.conn.commit()
        except Exception as e:
            print(f"Error al insertar reserva: {e}")
            raise

    def inicializar_base_datos(self):
        self.crear_tablas()
        self.insertar_usuarios_predeterminados()
        self.insertar_salas_predeterminadas()
        self.insertar_reservas_predeterminadas()
        self.conn.commit()

    def cerrar_conexion(self):
        self.conn.close()


if __name__ == "__main__":
    db_setup = DatabaseSetup()
    db_setup.inicializar_base_datos()
    db_setup.cerrar_conexion()