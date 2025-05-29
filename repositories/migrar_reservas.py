import sqlite3

def columna_existe(cursor, tabla, columna):
    cursor.execute(f"PRAGMA table_info({tabla})")
    return columna in [info[1] for info in cursor.fetchall()]

with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    # Agrega usuario_id
    if not columna_existe(cursor, "reservas", "usuario_id"):
        cursor.execute("ALTER TABLE reservas ADD COLUMN usuario_id INTEGER")
    # Agrega sala_id
    if not columna_existe(cursor, "reservas", "sala_id"):
        cursor.execute("ALTER TABLE reservas ADD COLUMN sala_id INTEGER")
    # Agrega fecha_inicio
    if not columna_existe(cursor, "reservas", "fecha_inicio"):
        cursor.execute("ALTER TABLE reservas ADD COLUMN fecha_inicio DATETIME")
    # Agrega fecha_fin
    if not columna_existe(cursor, "reservas", "fecha_fin"):
        cursor.execute("ALTER TABLE reservas ADD COLUMN fecha_fin DATETIME")
    conn.commit()

print("Migración completada. Las columnas faltantes fueron agregadas si era necesario.")