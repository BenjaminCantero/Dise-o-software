"""
Rutas para la gestión de reservas en SmartRoom API.
Incluye operaciones CRUD y utiliza comandos para la lógica de negocio.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..schemas.reserva import ReservaIn, ReservaOut
from ..services.reserva_service import ReservaService, UsuarioNoExisteError, SalaNoExisteError, ReservaNoExisteError
from api.commands.create_reserva_command import CreateReservaCommand
from api.commands.edit_reserva_command import EditReservaCommand
from api.commands.cancel_reserva_command import CancelReservaCommand
from api.commands.list_reservas_command import ListReservasCommand
from api.commands.get_reserva_command import GetReservaCommand

router = APIRouter(prefix="/reservas", tags=["reservas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_reserva_service():
    return ReservaService()

@router.get("/", response_model=list[ReservaOut])
def listar_reservas(
    db: Session = Depends(get_db),
    reserva_service: ReservaService = Depends(get_reserva_service)
):
    """Obtiene la lista de todas las reservas registradas."""
    reserva_service.db = db
    command = ListReservasCommand(reserva_service)
    reservas = command.execute()
    return [ReservaOut.from_orm(r) for r in reservas]

@router.get("/{reserva_id}", response_model=ReservaOut)
def get_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    reserva_service: ReservaService = Depends(get_reserva_service)
):
    """Obtiene una reserva por su ID."""
    reserva_service.db = db
    command = GetReservaCommand(reserva_service, reserva_id)
    reserva = command.execute()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return ReservaOut.from_orm(reserva)

@router.post("/", response_model=list[ReservaOut], status_code=201)
def create_reserva(
    reserva: ReservaIn,
    db: Session = Depends(get_db),
    reserva_service: ReservaService = Depends(get_reserva_service)
):
    """Crea una nueva reserva y retorna la lista actualizada."""
    reserva_service.db = db
    try:
        command = CreateReservaCommand(reserva_service, reserva.dict())
        command.execute()
        list_command = ListReservasCommand(reserva_service)
        reservas = list_command.execute()
        return [ReservaOut.from_orm(r) for r in reservas]
    except UsuarioNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SalaNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ReservaNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{reserva_id}", response_model=list[ReservaOut])
def update_reserva(
    reserva_id: int,
    reserva: ReservaIn,
    db: Session = Depends(get_db),
    reserva_service: ReservaService = Depends(get_reserva_service)
):
    """Actualiza una reserva existente y retorna la lista actualizada."""
    reserva_service.db = db
    try:
        command = EditReservaCommand(reserva_service, reserva_id, reserva.dict())
        command.execute()
        list_command = ListReservasCommand(reserva_service)
        reservas = list_command.execute()
        return [ReservaOut.from_orm(r) for r in reservas]
    except ReservaNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UsuarioNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SalaNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{reserva_id}", response_model=list[ReservaOut])
def delete_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    reserva_service: ReservaService = Depends(get_reserva_service)
):
    """Cancela una reserva por su ID y retorna la lista actualizada."""
    reserva_service.db = db
    try:
        command = CancelReservaCommand(reserva_service, reserva_id)
        command.execute()
        list_command = ListReservasCommand(reserva_service)
        reservas = list_command.execute()
        return [ReservaOut.from_orm(r) for r in reservas]
    except ReservaNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))