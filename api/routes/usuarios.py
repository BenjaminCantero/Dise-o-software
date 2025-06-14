from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models.usuario import Usuario
from ..schemas.usuario import UsuarioIn, UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

def adapt_usuario(usuario: Usuario):
    return UsuarioOut(
        id=usuario.id,
        username=usuario.username,
        role=usuario.role
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UsuarioOut])
def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return [adapt_usuario(u) for u in usuarios]

@router.get("/{usuario_id}", response_model=UsuarioOut)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return adapt_usuario(usuario)

@router.post("/", response_model=UsuarioOut, status_code=201)
def create_usuario(usuario: UsuarioIn, db: Session = Depends(get_db)):
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

@router.put("/{usuario_id}", response_model=UsuarioOut)
def update_usuario(usuario_id: int, usuario: UsuarioIn, db: Session = Depends(get_db)):
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

@router.delete("/{usuario_id}", response_model=list[UsuarioOut])
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    usuarios = db.query(Usuario).all()
    return [adapt_usuario(u) for u in usuarios]