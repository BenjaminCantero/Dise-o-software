import sqlite3

def crear_base_datos():
    # Conectar a la base de datos (se creará si no existe)
    conn = sqlite3.connect('gestion_salas.db')
    cursor = conn.cursor()

    # Crear tabla de salas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS salas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        capacidad INTEGER NOT NULL,
        estado TEXT NOT NULL
    )
    ''')

    # Crear tabla de reservas
    cursor.execute('''
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

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_base_datos()