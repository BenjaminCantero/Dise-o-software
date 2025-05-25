from repositories.db import SessionLocal
from repositories.user_repository import crear_usuario

def main():
    db = SessionLocal()
    username = input("Usuario: ")
    password = input("Contraseña: ")
    role = input("Rol (admin/profesor/estudiante): ").strip().lower()
    if role not in ["admin", "profesor", "estudiante"]:
        print("Rol no válido. Se asignará 'estudiante' por defecto.")
        role = "estudiante"
    nuevo_usuario = crear_usuario(db, username, password, role)
    print(f"Usuario creado: {nuevo_usuario}")

if __name__ == "__main__":
    main()