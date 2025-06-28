"""
Rutas de autenticación y login para SmartRoom API.
Permite a los usuarios obtener un token de acceso.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.db import SessionLocal
from api.models.usuario import Usuario

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    """Autentica al usuario y retorna sus datos si las credenciales son válidas."""
    username = data.get("username")
    password = data.get("password")
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if user and user.password == password:
        return {"id": user.id, "username": user.username, "role": user.role}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")