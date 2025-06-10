from fastapi import APIRouter, HTTPException
from services.sala_service import SalaService
from api.schemas.sala import SalaIn, SalaOut

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

@router.delete("/{sala_id}")
def delete_sala(sala_id: int):
    salas = sala_service.listar_salas()
    if not any(getattr(s, "id", s.get("id")) == sala_id for s in salas):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    sala_service.eliminar_sala(sala_id)
    return {"message": "Sala eliminada correctamente"}