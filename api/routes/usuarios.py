from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from api.db import SessionLocal
from api.models.usuario import Usuario
from api.schemas.usuario import UsuarioIn, UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

def adapt_usuario(usuario: Usuario):
    return UsuarioOut(
        id=usuario.id,
        username=usuario.username,
        role=usuario.role
    )

@router.get("/", response_model=list[UsuarioOut])
def get_usuarios():
    db = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        return [adapt_usuario(u) for u in usuarios]
    finally:
        db.close()

@router.get("/{usuario_id}", response_model=UsuarioOut)
def get_usuario(usuario_id: int):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter_by(id=usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return adapt_usuario(usuario)
    finally:
        db.close()

@router.post("/", response_model=UsuarioOut, status_code=201)
def create_usuario(usuario: UsuarioIn):
    db = SessionLocal()
    try:
        existente = db.query(Usuario).filter_by(username=usuario.username).first()
        if existente:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
        nuevo = Usuario(
            username=usuario.username,
            password=usuario.password,
            role=usuario.role
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return adapt_usuario(nuevo)
    finally:
        db.close()

@router.put("/{usuario_id}", response_model=UsuarioOut)
def update_usuario(usuario_id: int, usuario: UsuarioIn):
    db = SessionLocal()
    try:
        usuario_db = db.query(Usuario).filter_by(id=usuario_id).first()
        if not usuario_db:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        # Validar nombre de usuario único si cambia
        if usuario_db.username != usuario.username:
            existente = db.query(Usuario).filter_by(username=usuario.username).first()
            if existente:
                raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
        usuario_db.username = usuario.username
        usuario_db.password = usuario.password
        usuario_db.role = usuario.role
        db.commit()
        db.refresh(usuario_db)
        return adapt_usuario(usuario_db)
    finally:
        db.close()

@router.delete("/{usuario_id}", response_model=list[UsuarioOut])
def delete_usuario(usuario_id: int):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter_by(id=usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        db.delete(usuario)
        db.commit()
        usuarios = db.query(Usuario).all()
        return [adapt_usuario(u) for u in usuarios]
    finally:
        db.close()