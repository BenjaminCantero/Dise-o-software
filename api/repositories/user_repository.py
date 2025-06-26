from sqlalchemy.orm import Session
from api.models.usuario import Usuario
from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    def crear(self, db: Session, username: str, password: str, role: str = "estudiante"):
        usuario = Usuario(username=username, password=password, role=role)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    def obtener(self, db: Session, usuario_id: int):
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def actualizar(self, db: Session, usuario_id: int, username: str = None, password: str = None, role: str = None):
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if usuario:
            if username:
                usuario.username = username
            if password:
                usuario.password = password
            if role:
                usuario.role = role
            db.commit()
            db.refresh(usuario)
        return usuario

    def eliminar(self, db: Session, usuario_id: int):
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if usuario:
            db.delete(usuario)
            db.commit()
        return usuario

    # Métodos adicionales específicos
    def obtener_usuarios(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Usuario).offset(skip).limit(limit).all()

    def buscar_usuario_por_username(self, db: Session, username: str):
        return db.query(Usuario).filter(Usuario.username == username).first()