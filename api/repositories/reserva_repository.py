from sqlalchemy.orm import Session
from api.models.reserva import Reserva
from .base_repository import BaseRepository

class ReservaRepository(BaseRepository):

    def crear(self, db: Session, usuario_id: int, sala_id: int, fecha_inicio, fecha_fin):
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

    def obtener(self, db: Session, reserva_id: int):
        return db.query(Reserva).filter(Reserva.id == reserva_id).first()

    def actualizar(self, db: Session, reserva_id: int, usuario_id=None, sala_id=None,
                   fecha_inicio=None, fecha_fin=None):
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

    def eliminar(self, db: Session, reserva_id: int):
        reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if reserva:
            db.delete(reserva)
            db.commit()
        return reserva

    # Métodos adicionales específicos
    def obtener_reserva(self, db: Session, reserva_id: int):
        return self.obtener(db, reserva_id)

    def obtener_reservas(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Reserva).offset(skip).limit(limit).all()

    def listar_reservas(self, db: Session):
        return db.query(Reserva).all()