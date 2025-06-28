"""
Rutas para la gestión de salas en SmartRoom API.
Incluye operaciones CRUD y utiliza servicios para la lógica de negocio.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..schemas.sala import SalaIn, SalaOut
from ..services.sala_service import SalaService, SalaNoExisteError, NombreSalaYaExisteError
from ..db import SessionLocal

router = APIRouter(prefix="/salas", tags=["salas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sala_service():
    return SalaService()

@router.get("/", response_model=list[SalaOut])
def listar_salas(
    db: Session = Depends(get_db),
    sala_service: SalaService = Depends(get_sala_service)
):
    """Obtiene la lista de todas las salas registradas."""
    salas = sala_service.listar_salas(db)
    return [SalaOut.from_orm(s) for s in salas]

@router.get("/{sala_id}", response_model=SalaOut)
def get_sala(
    sala_id: int,
    db: Session = Depends(get_db),
    sala_service: SalaService = Depends(get_sala_service)
):
    """Obtiene una sala por su ID."""
    sala = sala_service.obtener_sala_por_id(db, sala_id)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return SalaOut.from_orm(sala)

@router.post("/", response_model=SalaOut, status_code=201)
def create_sala(
    sala: SalaIn,
    db: Session = Depends(get_db),
    sala_service: SalaService = Depends(get_sala_service)
):
    """Crea una nueva sala."""
    try:
        nueva_sala = sala_service.crear_sala(db, sala.nombre, sala.capacidad, sala.estado)
        return SalaOut.from_orm(nueva_sala)
    except NombreSalaYaExisteError as e:
        db.rollback()  # <-- ¡Agrega esto!
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error de base de datos")

@router.put("/{sala_id}", response_model=SalaOut)
def update_sala(
    sala_id: int,
    sala: SalaIn,
    db: Session = Depends(get_db),
    sala_service: SalaService = Depends(get_sala_service)
):
    """Actualiza una sala existente."""
    try:
        sala_actualizada = sala_service.editar_sala(db, sala_id, sala.nombre, sala.capacidad, sala.estado)
        return SalaOut.from_orm(sala_actualizada)
    except SalaNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NombreSalaYaExisteError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{sala_id}", response_model=list[SalaOut])
def delete_sala(
    sala_id: int,
    db: Session = Depends(get_db),
    sala_service: SalaService = Depends(get_sala_service)
):
    """Elimina una sala por su ID."""
    try:
        sala_service.eliminar_sala(db, sala_id)
        salas = sala_service.listar_salas(db)
        return [SalaOut.from_orm(s) for s in salas]
    except SalaNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))