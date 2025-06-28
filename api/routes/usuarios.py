"""
Rutas para la gestión de usuarios en SmartRoom API.
Incluye operaciones CRUD y utiliza dependencias para acceso a base de datos y servicios.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..schemas.usuario import UsuarioIn, UsuarioOut, UsuarioUpdate
from ..services.user_service import UserService, UsuarioNoExisteError, UsernameYaExisteError
from ..repositories.user_repository import UserRepository
from ..auth import get_current_user

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repository():
    return UserRepository()

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)

@router.get("/", response_model=list[UsuarioOut])
def get_usuarios(
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
    current_user: str = Depends(get_current_user)
):
    """Obtiene la lista de todos los usuarios registrados. Requiere autenticación JWT."""
    usuarios = user_service.listar_usuarios(db)
    return [UsuarioOut.from_orm(u) for u in usuarios]

@router.get("/{usuario_id}", response_model=UsuarioOut)
def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    """Obtiene un usuario por su ID."""
    usuarios = user_service.listar_usuarios(db)
    usuario = next((u for u in usuarios if u.id == usuario_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioOut.from_orm(usuario)

@router.post("/", response_model=UsuarioOut, status_code=201)
def create_usuario(
    usuario: UsuarioIn,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    """Crea un nuevo usuario con username, password y rol."""
    try:
        nuevo_usuario = user_service.crear_usuario(db, usuario.username, usuario.password, usuario.role)
        return UsuarioOut.from_orm(nuevo_usuario)
    except UsernameYaExisteError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{usuario_id}", response_model=UsuarioOut)
def update_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate, 
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    """Actualiza los datos de un usuario existente."""
    # --- DEPURACIÓN ---
    print("Datos recibidos para editar usuario:", usuario)
    print("Tipo de role:", type(usuario.role), "Valor de role:", usuario.role)
    # --- FIN DEPURACIÓN ---
    try:
        usuario_actualizado = user_service.editar_usuario(db, usuario_id, usuario.username, None, usuario.role)
        return UsuarioOut.from_orm(usuario_actualizado)
    except UsuarioNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UsernameYaExisteError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{usuario_id}", response_model=list[UsuarioOut])
def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    """Elimina un usuario por su ID y retorna la lista actualizada."""
    try:
        user_service.eliminar_usuario(db, usuario_id)
        usuarios = user_service.listar_usuarios(db)
        return [UsuarioOut.from_orm(u) for u in usuarios]
    except UsuarioNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))