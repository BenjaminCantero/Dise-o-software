from sqlalchemy.orm import Session
from .models import Reserva

def crear_reserva(db: Session, usuario_id: int, sala_id: int, fecha_inicio, fecha_fin):
    reserva = Reserva(
        usuario_id=usuario_id,
        sala_id=sala_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva

def obtener_reserva(db: Session, reserva_id: int):
    return db.query(Reserva).filter(Reserva.id == reserva_id).first()

def obtener_reservas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reserva).offset(skip).limit(limit).all()

def obtener_reservas_por_usuario(db: Session, usuario_id: int):
    return db.query(Reserva).filter(Reserva.usuario_id == usuario_id).all()

def actualizar_reserva(db: Session, reserva_id: int, fecha_inicio=None, fecha_fin=None):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if reserva:
        if fecha_inicio:
            reserva.fecha_inicio = fecha_inicio
        if fecha_fin:
            reserva.fecha_fin = fecha_fin
        db.commit()
        db.refresh(reserva)
    return reserva

def eliminar_reserva(db: Session, reserva_id: int):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if reserva:
        db.delete(reserva)
        db.commit()
    return reserva