from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..schemas.reserva import ReservaIn, ReservaOut
from ..services.reserva_service import ReservaService, UsuarioNoExisteError, SalaNoExisteError, ReservaNoExisteError

router = APIRouter(prefix="/reservas", tags=["reservas"])

reserva_service = ReservaService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ReservaOut])
def get_reservas(db: Session = Depends(get_db)):
    reservas = reserva_service.listar_reservas(db)
    return [ReservaOut.from_orm(r) for r in reservas]

@router.get("/{reserva_id}", response_model=ReservaOut)
def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = reserva_service.obtener_reserva_por_id(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return ReservaOut.from_orm(reserva)

@router.post("/", response_model=list[ReservaOut], status_code=201)
def create_reserva(reserva: ReservaIn, db: Session = Depends(get_db)):
    try:
        nueva_reserva = reserva_service.crear_reserva(
            db,
            usuario_id=reserva.usuario_id,
            sala_id=reserva.sala_id,
            fecha_inicio=reserva.fecha_inicio,
            fecha_fin=reserva.fecha_fin
        )
        reservas = reserva_service.listar_reservas(db)
        return [ReservaOut.from_orm(r) for r in reservas]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{reserva_id}", response_model=list[ReservaOut])
def update_reserva(reserva_id: int, reserva: ReservaIn, db: Session = Depends(get_db)):
    try:
        reserva_service.editar_reserva(
            db,
            reserva_id,
            usuario_id=reserva.usuario_id,
            sala_id=reserva.sala_id,
            fecha_inicio=reserva.fecha_inicio,
            fecha_fin=reserva.fecha_fin
        )
        reservas = reserva_service.listar_reservas(db)
        return [ReservaOut.from_orm(r) for r in reservas]
    except UsuarioNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SalaNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ReservaNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{reserva_id}", response_model=list[ReservaOut])
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva_service.eliminar_reserva(db, reserva_id)
    reservas = reserva_service.listar_reservas(db)
    return [ReservaOut.from_orm(r) for r in reservas]