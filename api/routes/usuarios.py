from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..schemas.usuario import UsuarioIn, UsuarioOut
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

user_service = UserService(UserRepository())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UsuarioOut])
def get_usuarios(db: Session = Depends(get_db)):
    return user_service.listar_usuarios(db)

@router.get("/{usuario_id}", response_model=UsuarioOut)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuarios = user_service.listar_usuarios(db)
    usuario = next((u for u in usuarios if u.id == usuario_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioOut, status_code=201)
def create_usuario(usuario: UsuarioIn, db: Session = Depends(get_db)):
    try:
        return user_service.crear_usuario(db, usuario.username, usuario.password, usuario.role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{usuario_id}", response_model=UsuarioOut)
def update_usuario(usuario_id: int, usuario: UsuarioIn, db: Session = Depends(get_db)):
    try:
        return user_service.editar_usuario(db, usuario_id, usuario.username, usuario.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{usuario_id}", response_model=list[UsuarioOut])
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    user_service.eliminar_usuario(db, usuario_id)
    return user_service.listar_usuarios(db)