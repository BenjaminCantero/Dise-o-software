from core.observable import Observable
from repositories.db import SessionLocal
from repositories.models import Usuario

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class UserService(Observable):
    def __init__(self):
        super().__init__()

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

    # Métodos para observer
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
        if username in self.usuarios:
            del self.usuarios[username]
            self.notify_observers(event="usuario_eliminado", data=username)

    def editar_usuario(self, username, role, password=None):
        db = SessionLocal()
        usuario_db = db.query(Usuario).filter_by(username=username).first()
        if usuario_db:
            usuario_db.role = role
            if password:
                usuario_db.password = password
            db.commit()
        db.close()