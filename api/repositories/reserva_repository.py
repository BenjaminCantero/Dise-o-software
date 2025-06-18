from sqlalchemy.orm import Session
from api.models.reserva import Reserva

class ReservaRepository:
    def crear_reserva(self, db: Session, usuario_id: int, sala_id: int, fecha_inicio, fecha_fin):
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

    def obtener_reserva(self, db: Session, reserva_id: int):
        return db.query(Reserva).filter(Reserva.id == reserva_id).first()

    def obtener_reservas(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Reserva).offset(skip).limit(limit).all()

    def obtener_reservas_por_usuario(self, db: Session, usuario_id: int):
        return db.query(Reserva).filter(Reserva.usuario_id == usuario_id).all()

    def actualizar_reserva(self, db: Session, reserva_id: int, usuario_id=None, sala_id=None, fecha_inicio=None, fecha_fin=None):
        reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if reserva:
            if usuario_id is not None:
                reserva.usuario_id = usuario_id
            if sala_id is not None:
                reserva.sala_id = sala_id
            if fecha_inicio is not None:
                reserva.fecha_inicio = fecha_inicio
            if fecha_fin is not None:
                reserva.fecha_fin = fecha_fin
            db.commit()
            db.refresh(reserva)
        return reserva

    def eliminar_reserva(self, db: Session, reserva_id: int):
        reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if reserva:
            db.delete(reserva)
            db.commit()
        return reserva