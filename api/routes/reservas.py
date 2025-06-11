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
    # Validar sala existente
    salas = sala_service.listar_salas()
    if not any(getattr(s, "nombre", s.get("nombre")) == reserva.sala_nombre for s in salas):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    # Validar usuario existente
    usuarios = user_service.listar_usuarios()
    if not any(getattr(u, "username", u.get("username")) == reserva.usuario_username for u in usuarios):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Validar fechas no nulas y orden correcto
    if reserva.fecha_inicio is None or reserva.fecha_fin is None:
        raise HTTPException(status_code=400, detail="Las fechas no pueden ser nulas")
    if reserva.fecha_inicio >= reserva.fecha_fin:
        raise HTTPException(status_code=400, detail="La fecha de inicio debe ser anterior a la fecha de fin")
    # Validar que la sala esté disponible en ese horario
    reservas_existentes = reserva_service.listar_reservas()
    for r in reservas_existentes:
        if r["sala"] == reserva.sala_nombre:
            # Solapamiento de horarios
            if not (reserva.fecha_fin <= r["fecha"] or reserva.fecha_inicio >= r["fecha"]):
                raise HTTPException(status_code=400, detail="La sala ya está reservada en ese horario")
    # (Opcional) Validar que el usuario no tenga otra reserva en ese horario
    for r in reservas_existentes:
        if r["usuario"] == reserva.usuario_username:
            if not (reserva.fecha_fin <= r["fecha"] or reserva.fecha_inicio >= r["fecha"]):
                raise HTTPException(status_code=400, detail="El usuario ya tiene una reserva en ese horario")
    # Crear reserva
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

@router.delete("/{reserva_id}", response_model=list[ReservaOut])
def delete_reserva(reserva_id: int):
    try:
        reserva_service.eliminar_reserva(reserva_id)
        reservas = reserva_service.listar_reservas()
        return reservas
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error al eliminar reserva: {e}")  # <-- Esto te mostrará el error real en consola
        raise HTTPException(status_code=500, detail="Error interno del servidor")