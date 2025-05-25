from repositories.db import SessionLocal
from repositories.user_repository import crear_usuario

def main():
    db = SessionLocal()
    usuario = input("Usuario: ")
    password = input("Contraseña: ")
    nuevo_usuario = crear_usuario(db, usuario, password)
    print(f"Usuario creado: {nuevo_usuario}")

if __name__ == "__main__":
    main()