from fastapi import APIRouter, HTTPException
from services.reserva_service import ReservaService
from services.sala_service import SalaService
from services.user_service import UserService
from api.schemas.reserva import ReservaIn, ReservaOut

from datetime import datetime, timedelta, timezone

def adapt_reserva(reserva):
    if "sala_nombre" in reserva:
        return reserva
    fecha = reserva.get("fecha")
    hora = reserva.get("hora")
    # Si tienes duración, úsala, si no, suma 1 hora por defecto
    if fecha and hora:
        fecha_inicio = datetime.fromisoformat(f"{fecha}T{hora}")
        fecha_fin = fecha_inicio + timedelta(hours=1)
    else:
        fecha_inicio = reserva.get("fecha_inicio")
        fecha_fin = reserva.get("fecha_fin")
    return {
        "id": reserva.get("id"),
        "sala_nombre": reserva.get("sala") or reserva.get("sala_nombre"),
        "usuario_username": reserva.get("usuario") or reserva.get("usuario_username"),
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    }

def to_naive(dt):
    if dt is not None and hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt

router = APIRouter(prefix="/reservas", tags=["reservas"])
reserva_service = ReservaService()
sala_service = SalaService()
user_service = UserService()

@router.get("/", response_model=list[ReservaOut])
def get_reservas():
    reservas = reserva_service.listar_reservas()
    return [adapt_reserva(r) for r in reservas]

@router.get("/{reserva_id}", response_model=ReservaOut)
def get_reserva(reserva_id: int):
    reserva = reserva_service.obtener_reserva_por_id(reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return adapt_reserva(reserva)

@router.post("/", response_model=ReservaOut, status_code=201)
def create_reserva(reserva: ReservaIn):
    # Validar sala existente
    salas = sala_service.listar_salas()
    if not any(
        (getattr(s, "nombre", None) or (s.get("nombre") if isinstance(s, dict) else None)) == reserva.sala_nombre
        for s in salas
    ):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    # Validar usuario existente
    usuarios = user_service.listar_usuarios()
    if not any(
        (getattr(u, "username", None) or (u.get("username") if isinstance(u, dict) else None)) == reserva.usuario_username
        for u in usuarios
    ):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Validar fechas no nulas y orden correcto
    if reserva.fecha_inicio is None or reserva.fecha_fin is None:
        raise HTTPException(status_code=400, detail="Las fechas no pueden ser nulas")
    if reserva.fecha_inicio >= reserva.fecha_fin:
        raise HTTPException(status_code=400, detail="La fecha de inicio debe ser anterior a la fecha de fin")
    # Validar que la sala esté disponible en ese horario
    reservas_existentes = reserva_service.listar_reservas()
    for r in reservas_existentes:
        r_sala_nombre = r.get("sala_nombre") if isinstance(r, dict) else getattr(r, "sala_nombre", None)
        r_fecha_inicio = to_naive(r.get("fecha_inicio") if isinstance(r, dict) else getattr(r, "fecha_inicio", None))
        r_fecha_fin = to_naive(r.get("fecha_fin") if isinstance(r, dict) else getattr(r, "fecha_fin", None))
        fecha_inicio = to_naive(reserva.fecha_inicio)
        fecha_fin = to_naive(reserva.fecha_fin)
        if r_sala_nombre == reserva.sala_nombre:
            if not (fecha_fin <= r_fecha_inicio or fecha_inicio >= r_fecha_fin):
                raise HTTPException(status_code=400, detail="La sala ya está reservada en ese horario")
    # (Opcional) Validar que el usuario no tenga otra reserva en ese horario
    for r in reservas_existentes:
        r_usuario_username = r.get("usuario_username") if isinstance(r, dict) else getattr(r, "usuario_username", None)
        r_fecha_inicio = to_naive(r.get("fecha_inicio") if isinstance(r, dict) else getattr(r, "fecha_inicio", None))
        r_fecha_fin = to_naive(r.get("fecha_fin") if isinstance(r, dict) else getattr(r, "fecha_fin", None))
        fecha_inicio = to_naive(reserva.fecha_inicio)
        fecha_fin = to_naive(reserva.fecha_fin)
        if r_usuario_username == reserva.usuario_username:
            if not (fecha_fin <= r_fecha_inicio or fecha_inicio >= r_fecha_fin):
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

@router.put("/{reserva_id}", response_model=list[ReservaOut])
def update_reserva(reserva_id: int, reserva: ReservaIn):
    # Validar sala existente
    salas = sala_service.listar_salas()
    if not any(
        (getattr(s, "nombre", None) or (s.get("nombre") if isinstance(s, dict) else None)) == reserva.sala_nombre
        for s in salas
    ):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    # Validar usuario existente
    usuarios = user_service.listar_usuarios()
    if not any(
        (getattr(u, "username", None) or (u.get("username") if isinstance(u, dict) else None)) == reserva.usuario_username
        for u in usuarios
    ):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Validar fechas no nulas y orden correcto
    if reserva.fecha_inicio is None or reserva.fecha_fin is None:
        raise HTTPException(status_code=400, detail="Las fechas no pueden ser nulas")
    if reserva.fecha_inicio >= reserva.fecha_fin:
        raise HTTPException(status_code=400, detail="La fecha de inicio debe ser anterior a la fecha de fin")
    # Validar que la sala esté disponible en ese horario (ignorando la reserva actual)
    reservas_existentes = reserva_service.listar_reservas()
    for r in reservas_existentes:
        r_id = r.get("id") if isinstance(r, dict) else getattr(r, "id", None)
        r_sala_nombre = r.get("sala_nombre") if isinstance(r, dict) else getattr(r, "sala_nombre", None)
        r_fecha_inicio = to_naive(r.get("fecha_inicio") if isinstance(r, dict) else getattr(r, "fecha_inicio", None))
        r_fecha_fin = to_naive(r.get("fecha_fin") if isinstance(r, dict) else getattr(r, "fecha_fin", None))
        fecha_inicio = to_naive(reserva.fecha_inicio)
        fecha_fin = to_naive(reserva.fecha_fin)
        if r_id != reserva_id and r_sala_nombre == reserva.sala_nombre:
            if not (fecha_fin <= r_fecha_inicio or fecha_inicio >= r_fecha_fin):
                raise HTTPException(status_code=400, detail="La sala ya está reservada en ese horario")
    # Validar que el usuario no tenga otra reserva en ese horario (ignorando la reserva actual)
    for r in reservas_existentes:
        r_id = r.get("id") if isinstance(r, dict) else getattr(r, "id", None)
        r_usuario_username = r.get("usuario_username") if isinstance(r, dict) else getattr(r, "usuario_username", None)
        r_fecha_inicio = to_naive(r.get("fecha_inicio") if isinstance(r, dict) else getattr(r, "fecha_inicio", None))
        r_fecha_fin = to_naive(r.get("fecha_fin") if isinstance(r, dict) else getattr(r, "fecha_fin", None))
        fecha_inicio = to_naive(reserva.fecha_inicio)
        fecha_fin = to_naive(reserva.fecha_fin)
        if r_id != reserva_id and r_usuario_username == reserva.usuario_username:
            if not (fecha_fin <= r_fecha_inicio or fecha_inicio >= r_fecha_fin):
                raise HTTPException(status_code=400, detail="El usuario ya tiene una reserva en ese horario")
    # Editar reserva
    try:
        reserva_service.editar_reserva(
            reserva_id=reserva_id,
            sala_nombre=reserva.sala_nombre,
            usuario_username=reserva.usuario_username,
            fecha_inicio=reserva.fecha_inicio,
            fecha_fin=reserva.fecha_fin
        )
        # Devuelve la lista de reservas actualizada
        return reserva_service.listar_reservas()
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