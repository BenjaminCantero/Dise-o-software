from fastapi import APIRouter, HTTPException
from services.reserva_service import ReservaService
from services.sala_service import SalaService
from services.user_service import UserService
from api.schemas.reserva import ReservaIn, ReservaOut

router = APIRouter(prefix="/reservas", tags=["reservas"])
reserva_service = ReservaService()
sala_service = SalaService()
user_service = UserService()

@router.get("/", response_model=list[ReservaOut])
def get_reservas():
    return reserva_service.listar_reservas()

@router.get("/{reserva_id}", response_model=ReservaOut)
def get_reserva(reserva_id: int):
    reserva = reserva_service.obtener_reserva_por_id(reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.post("/", response_model=ReservaOut, status_code=201)
def create_reserva(reserva: ReservaIn):
    salas = sala_service.listar_salas()
    if not any(getattr(s, "nombre", s.get("nombre")) == reserva.sala_nombre for s in salas):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    usuarios = user_service.listar_usuarios()
    if not any(getattr(u, "username", u.get("username")) == reserva.usuario_username for u in usuarios):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    try:
        nueva = reserva_service.crear_reserva(
            sala_nombre=reserva.sala_nombre,
            usuario_username=reserva.usuario_username,
            fecha_inicio=reserva.fecha_inicio,
            fecha_fin=reserva.fecha_fin
        )
        return nueva
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/{reserva_id}")
def update_reserva(reserva_id: int, reserva: ReservaIn):
    try:
        reserva_service.editar_reserva(
            reserva_id=reserva_id,
            sala_nombre=reserva.sala_nombre,
            usuario_username=reserva.usuario_username,
            fecha_inicio=reserva.fecha_inicio,
            fecha_fin=reserva.fecha_fin
        )
        return {"message": "Reserva actualizada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.delete("/{reserva_id}")
def delete_reserva(reserva_id: int):
    try:
        reserva_service.eliminar_reserva(reserva_id)
        return {"message": "Reserva eliminada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")