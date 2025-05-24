from sqlalchemy.orm import Session
from .models import Usuario

def crear_usuario(db: Session, nombre: str, email: str):
    usuario = Usuario(nombre=nombre, email=email)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def actualizar_usuario(db: Session, usuario_id: int, nombre: str = None, email: str = None):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        if nombre:
            usuario.nombre = nombre
        if email:
            usuario.email = email
        db.commit()
        db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario