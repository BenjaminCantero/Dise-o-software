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

@router.post("/", response_model=SalaOut, status_code=201)
def create_sala(sala: SalaIn):
    nueva = sala_service.crear_sala(
        nombre=sala.nombre,
        capacidad=sala.capacidad,
        estado=sala.estado
    )
    return nueva

@router.put("/{sala_id}")
def update_sala(sala_id: int, sala: SalaIn):
    salas = sala_service.listar_salas()
    if not any(getattr(s, "id", s.get("id")) == sala_id for s in salas):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    sala_service.editar_sala(
        sala_id=sala_id,
        nombre=sala.nombre,
        capacidad=sala.capacidad,
        estado=sala.estado
    )
    return {"message": "Sala actualizada correctamente"}

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