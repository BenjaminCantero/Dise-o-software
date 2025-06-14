# services/reserva_service.py
from smartroom.core.observable import Observable
from smartroom.core.singleton import SingletonMeta
from api.db import SessionLocal
from api.models import Reserva, Usuario, Sala
from smartroom.builders.reserva_builder import ReservaBuilder
from smartroom.decorators.notificacion_reserva import ReservaNotificada  # Decorator importado

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
                    "sala_nombre": r.sala.nombre if r.sala else "",
                    "usuario_username": r.usuario.username if r.usuario else "",
                    "fecha_inicio": r.fecha_inicio,
                    "fecha_fin": r.fecha_fin,
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

            nueva_reserva = (
                ReservaBuilder()
                    .set_usuario(usuario)
                    .set_sala(sala)
                    .set_fecha_inicio(fecha_inicio)
                    .set_fecha_fin(fecha_fin)
                    .build()
                )
            db.add(nueva_reserva)
            db.commit()
            db.refresh(nueva_reserva)
            self.notify_observers(event="reserva_creada", data=nueva_reserva)
            # Devuelve un dict con los datos completos ANTES de cerrar la sesión
            reserva_dict = {
                "id": nueva_reserva.id,
                "sala_nombre": nueva_reserva.sala.nombre if nueva_reserva.sala else "",
                "usuario_username": nueva_reserva.usuario.username if nueva_reserva.usuario else "",
                "fecha_inicio": nueva_reserva.fecha_inicio,
                "fecha_fin": nueva_reserva.fecha_fin,
            }
            return reserva_dict
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
                print(f"Reserva con id {reserva_id} no encontrada para eliminar.")  # Debug
                raise ValueError("Reserva no encontrada.")
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
            # Notificar con un diccionario, no con el objeto
            reserva_dict = {
                "id": reserva.id,
                "sala": sala.nombre,
                "usuario": usuario.username,
                "fecha": reserva.fecha_inicio.strftime("%Y-%m-%d"),
                "hora": reserva.fecha_inicio.strftime("%H:%M"),
                "estado": reserva.estado if hasattr(reserva, "estado") else "N/A"
            }
            self.notify_observers(event="reserva_editada", data=reserva_dict)
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

    def obtener_reserva_por_id(self, reserva_id):
        db = SessionLocal()
        try:
            reserva = db.query(Reserva).filter_by(id=reserva_id).first()
            if reserva:
                return {
                    "id": reserva.id,
                    "sala": reserva.sala.nombre if reserva.sala else "",
                    "usuario": reserva.usuario.username if reserva.usuario else "",
                    "fecha": reserva.fecha_inicio.strftime("%Y-%m-%d"),
                    "hora": reserva.fecha_inicio.strftime("%H:%M"),
                    "estado": reserva.estado if hasattr(reserva, "estado") else "N/A"
                }
            return None
        finally:
            db.close()

    def eliminar_reservas_por_usuario(self, username):
        db = SessionLocal()
        try:
            usuario = db.query(Usuario).filter_by(username=username).first()
            if usuario:
                reservas = db.query(Reserva).filter_by(usuario_id=usuario.id).all()
                for reserva in reservas:
                    db.delete(reserva)
                db.commit()
        finally:
            db.close()