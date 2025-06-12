from sqlalchemy.orm import Session
from .models import Usuario

def crear_usuario(db: Session, username: str, password: str, role: str = "estudiante"):
    usuario = Usuario(username=username, password=password, role=role)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def actualizar_usuario(db: Session, usuario_id: int, username: str = None, password: str = None):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        if username:
            usuario.username = username
        if password:
            usuario.password = password
        db.commit()
        db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario

def buscar_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def buscar_usuario_por_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()