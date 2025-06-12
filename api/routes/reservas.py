from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from api.db import SessionLocal
from api.models import Reserva, Sala, Usuario
from api.schemas.reserva import ReservaIn, ReservaOut

router = APIRouter(prefix="/reservas", tags=["reservas"])

def adapt_reserva(reserva: Reserva):
    return ReservaOut(
        id=reserva.id,
        sala_nombre=reserva.sala.nombre if reserva.sala else None,
        usuario_username=reserva.usuario.username if reserva.usuario else None,
        fecha_inicio=reserva.fecha_inicio,
        fecha_fin=reserva.fecha_fin,
    )

@router.get("/", response_model=list[ReservaOut])
def get_reservas():
    db = SessionLocal()
    try:
        reservas = db.query(Reserva).all()
        for r in reservas:
            _ = r.sala
            _ = r.usuario
        return [adapt_reserva(r) for r in reservas]
    finally:
        db.close()

@router.get("/{reserva_id}", response_model=ReservaOut)
def get_reserva(reserva_id: int):
    db = SessionLocal()
    try:
        reserva = db.query(Reserva).filter_by(id=reserva_id).first()
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        _ = reserva.sala
        _ = reserva.usuario
        return adapt_reserva(reserva)
    finally:
        db.close()

@router.post("/", response_model=ReservaOut, status_code=201)
def create_reserva(reserva: ReservaIn):
    db = SessionLocal()
    try:
        sala = db.query(Sala).filter_by(nombre=reserva.sala_nombre).first()
        if not sala:
            raise HTTPException(status_code=404, detail="Sala no encontrada")
        usuario = db.query(Usuario).filter_by(username=reserva.usuario_username).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if reserva.fecha_inicio is None or reserva.fecha_fin is None:
            raise HTTPException(status_code=400, detail="Las fechas no pueden ser nulas")
        if reserva.fecha_inicio >= reserva.fecha_fin:
            raise HTTPException(status_code=400, detail="La fecha de inicio debe ser anterior a la fecha de fin")
        # Validar solapamiento de reservas
        solapada = db.query(Reserva).filter(
            Reserva.sala_id == sala.id,
            Reserva.fecha_fin > reserva.fecha_inicio,
            Reserva.fecha_inicio < reserva.fecha_fin
        ).first()
        if solapada:
            raise HTTPException(status_code=400, detail="La sala ya está reservada en ese horario")
        solapada_usuario = db.query(Reserva).filter(
            Reserva.usuario_id == usuario.id,
            Reserva.fecha_fin > reserva.fecha_inicio,
            Reserva.fecha_inicio < reserva.fecha_fin
        ).first()
        if solapada_usuario:
            raise HTTPException(status_code=400, detail="El usuario ya tiene una reserva en ese horario")
        nueva = Reserva(
            sala_id=sala.id,
            usuario_id=usuario.id,
            fecha_inicio=reserva.fecha_inicio,
            fecha_fin=reserva.fecha_fin
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        _ = nueva.sala
        _ = nueva.usuario
        return adapt_reserva(nueva)
    finally:
        db.close()

@router.put("/{reserva_id}", response_model=list[ReservaOut])
def update_reserva(reserva_id: int, reserva: ReservaIn):
    db = SessionLocal()
    try:
        sala = db.query(Sala).filter_by(nombre=reserva.sala_nombre).first()
        if not sala:
            raise HTTPException(status_code=404, detail="Sala no encontrada")
        usuario = db.query(Usuario).filter_by(username=reserva.usuario_username).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if reserva.fecha_inicio is None or reserva.fecha_fin is None:
            raise HTTPException(status_code=400, detail="Las fechas no pueden ser nulas")
        if reserva.fecha_inicio >= reserva.fecha_fin:
            raise HTTPException(status_code=400, detail="La fecha de inicio debe ser anterior a la fecha de fin")
        reserva_db = db.query(Reserva).filter_by(id=reserva_id).first()
        if not reserva_db:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        # Validar solapamiento de reservas (excluyendo la actual)
        solapada = db.query(Reserva).filter(
            Reserva.id != reserva_id,
            Reserva.sala_id == sala.id,
            Reserva.fecha_fin > reserva.fecha_inicio,
            Reserva.fecha_inicio < reserva.fecha_fin
        ).first()
        if solapada:
            raise HTTPException(status_code=400, detail="La sala ya está reservada en ese horario")
        solapada_usuario = db.query(Reserva).filter(
            Reserva.id != reserva_id,
            Reserva.usuario_id == usuario.id,
            Reserva.fecha_fin > reserva.fecha_inicio,
            Reserva.fecha_inicio < reserva.fecha_fin
        ).first()
        if solapada_usuario:
            raise HTTPException(status_code=400, detail="El usuario ya tiene una reserva en ese horario")
        reserva_db.sala_id = sala.id
        reserva_db.usuario_id = usuario.id
        reserva_db.fecha_inicio = reserva.fecha_inicio
        reserva_db.fecha_fin = reserva.fecha_fin
        db.commit()
        reservas = db.query(Reserva).all()
        for r in reservas:
            _ = r.sala
            _ = r.usuario
        return [adapt_reserva(r) for r in reservas]
    finally:
        db.close()

@router.delete("/{reserva_id}", response_model=list[ReservaOut])
def delete_reserva(reserva_id: int):
    db = SessionLocal()
    try:
        reserva = db.query(Reserva).filter_by(id=reserva_id).first()
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        db.delete(reserva)
        db.commit()
        reservas = db.query(Reserva).all()
        for r in reservas:
            _ = r.sala
            _ = r.usuario
        return [adapt_reserva(r) for r in reservas]
    finally:
        db.close()