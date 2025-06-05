# services/reserva_service.py
from core.observable import Observable
from core.singleton import SingletonMeta
from repositories.db import SessionLocal
from repositories.models import Reserva, Usuario, Sala
from builders.reserva_builder import ReservaBuilder
from decorators.notificacion_reserva import ReservaNotificada  # Decorator importado

class ReservaService(Observable, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()

    def listar_reservas(self):
        db = SessionLocal()
        try:
            reservas = db.query(Reserva).all()
            resultado = []
            for r in reservas:
                resultado.append({
                    "id": r.id,
                    "sala": r.sala.nombre if r.sala else "",
                    "usuario": r.usuario.username if r.usuario else "",
                    "fecha": r.fecha_inicio.strftime("%Y-%m-%d"),
                    "hora": r.fecha_inicio.strftime("%H:%M"),
                    "estado": r.estado if hasattr(r, "estado") else "N/A"
                })
            return resultado
        finally:
            db.close()

    def crear_reserva(self, sala_nombre, usuario_username, fecha_inicio, fecha_fin):
        db = SessionLocal()
        try:
            usuario = db.query(Usuario).filter_by(username=usuario_username).first()
            sala = db.query(Sala).filter_by(nombre=sala_nombre).first()

            if not usuario or not sala:
                raise Exception("Usuario o sala no encontrados.")

            existe = db.query(Reserva).filter(
                Reserva.sala_id == sala.id,
                Reserva.fecha_inicio < fecha_fin,
                Reserva.fecha_fin > fecha_inicio
            ).first()

            if existe:
                raise Exception("La sala ya está reservada en ese horario.")

            nueva_reserva = Reserva(
                usuario_id=usuario.id,
                sala_id=sala.id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            db.add(nueva_reserva)
            db.commit()
            db.refresh(nueva_reserva)
            self.notify_observers(event="reserva_creada", data=nueva_reserva)
            return nueva_reserva
        finally:
            db.close()

    def eliminar_reserva(self, reserva_id):
        db = SessionLocal()
        try:
            reserva = db.query(Reserva).filter_by(id=reserva_id).first()
            if reserva:
                db.delete(reserva)
                db.commit()
                self.notify_observers(event="reserva_eliminada", data=reserva_id)
            else:
                raise Exception("Reserva no encontrada.")
        finally:
            db.close()

    def contar_reservas(self):
        db = SessionLocal()
        try:
            count = db.query(Reserva).count()
            return count
        finally:
            db.close()

    def obtener_reservas_por_usuario(self, username):
        todas = self.listar_reservas()
        return [r for r in todas if r.get("usuario") == username]

    def editar_reserva(self, reserva_id, sala_nombre, usuario_username, fecha_inicio, fecha_fin):
        db = SessionLocal()
        try:
            reserva = db.query(Reserva).filter_by(id=reserva_id).first()
            usuario = db.query(Usuario).filter_by(username=usuario_username).first()
            sala = db.query(Sala).filter_by(nombre=sala_nombre).first()

            if not reserva or not usuario or not sala:
                raise Exception("Reserva, usuario o sala no encontrados.")

            reserva.usuario_id = usuario.id
            reserva.sala_id = sala.id
            reserva.fecha_inicio = fecha_inicio
            reserva.fecha_fin = fecha_fin
            db.commit()
            self.notify_observers(event="reserva_editada", data=reserva)
            return reserva
        finally:
            db.close()

    def agregar_reserva(self, usuario, sala, fecha_inicio, fecha_fin):
        builder = ReservaBuilder()
        reserva = (
            builder
            .set_usuario(usuario)
            .set_sala(sala)
            .set_fecha_inicio(fecha_inicio)
            .set_fecha_fin(fecha_fin)
            .build()
        )
        # --- Uso del patrón Decorator ---
        reserva_decorada = ReservaNotificada(reserva)
        reserva_decorada.confirmar()
