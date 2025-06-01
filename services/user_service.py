# services/user_service.py
from core.observable import Observable
from core.singleton import SingletonMeta # <--- IMPORTADO para Singleton
from repositories.db import SessionLocal
from repositories.models import Usuario

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class UserService(Observable, metaclass=SingletonMeta): # <--- METACLASE AÑADIDA para Singleton
    def __init__(self):
        super().__init__() # Inicialización de Observable
        print("UserService Singleton Inicializado") # Demuestra que __init__ se llama una vez
        # Lógica de inicialización original de UserService

    def autenticar(self, username, password):
        db = SessionLocal()
        user_db = db.query(Usuario).filter_by(username=username, password=password).first()
        db.close()
        if user_db:
            return User(user_db.username, user_db.role)
        return None

    def listar_usuarios(self):
        db = SessionLocal()
        usuarios_db = db.query(Usuario).all()
        usuarios = [User(u.username, u.role) for u in usuarios_db]
        db.close()
        return usuarios

    def crear_usuario(self, username, password, role):
        db = SessionLocal()
        nuevo_usuario = Usuario(username=username, password=password, role=role)
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        db.close()
        self.notify_observers(event="usuario_creado", data=nuevo_usuario)
        return nuevo_usuario

    def eliminar_usuario(self, username):
        db = SessionLocal()
        usuario_db = db.query(Usuario).filter_by(username=username).first()
        if usuario_db:
            db.delete(usuario_db)
            db.commit()
            self.notify_observers(event="usuario_eliminado", data=username)
        db.close()

    def editar_usuario(self, username, role):
        db = SessionLocal()
        usuario_db = db.query(Usuario).filter_by(username=username).first()
        if usuario_db:
            usuario_db.role = role
            db.commit()
            self.notify_observers(event="usuario_editado", data={"username": username, "role": role})
        db.close()
