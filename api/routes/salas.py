from fastapi import APIRouter, HTTPException
from services.sala_service import SalaService
from api.schemas.sala import SalaIn, SalaOut
from sqlalchemy.orm import Session
from repositories.db import SessionLocal
from repositories.models import Reserva

router = APIRouter(prefix="/salas", tags=["salas"])
sala_service = SalaService()

@router.get("/", response_model=list[SalaOut])
def get_salas():
    return sala_service.listar_salas()

@router.post("/", response_model=list[SalaOut], status_code=201)
def create_sala(sala_data: SalaIn):
    # Validar estado
    if sala_data.estado.lower() not in ["ocupada", "disponible"]:
        raise HTTPException(
            status_code=400,
            detail="Agregue un estado válido: 'ocupada' o 'disponible'"
        )
    # Validar nombre único
    salas = sala_service.listar_salas()
    if any(
        (getattr(s, "nombre", None) or (s.get("nombre") if isinstance(s, dict) else None)).lower() == sala_data.nombre.lower()
        for s in salas
    ):
        raise HTTPException(
            status_code=400,
            detail="Ya existe una sala con ese nombre"
        )
    try:
        sala_service.crear_sala(
            nombre=sala_data.nombre,
            capacidad=sala_data.capacidad,
            estado=sala_data.estado.lower()
        )
        salas = sala_service.listar_salas()
        return salas
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/{sala_id}", response_model=list[SalaOut])
def update_sala(sala_id: int, sala_data: SalaIn):
    # Validación del estado
    if sala_data.estado.lower() not in ["ocupada", "disponible"]:
        raise HTTPException(
            status_code=400,
            detail="Agregue un estado válido: 'ocupada' o 'disponible'"
        )
    try:
        sala_service.editar_sala(
            sala_id=sala_id,
            nombre=sala_data.nombre,
            capacidad=sala_data.capacidad,
            estado=sala_data.estado.lower()
        )
        salas = sala_service.listar_salas()
        return salas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.delete("/{sala_id}", response_model=list[SalaOut])
def delete_sala(sala_id: int):
    sala = sala_service.obtener_sala_por_id(sala_id)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    # Consulta directa para contar reservas
    db: Session = SessionLocal()
    try:
        reservas_count = db.query(Reserva).filter(Reserva.sala_id == sala_id).count()
    finally:
        db.close()
    if reservas_count > 0:
        raise HTTPException(status_code=400, detail="No se puede eliminar una sala con reservas activas")
    try:
        sala_service.eliminar_sala(sala_id)
        salas = sala_service.listar_salas()
        return salas
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")