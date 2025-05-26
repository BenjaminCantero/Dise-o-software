from core.observable import Observable

class ReservaService(Observable):
    def __init__(self):
        super().__init__()
        # Aquí puedes inicializar una lista de reservas o conectar con el repositorio
        self.reservas = []

    def listar_reservas(self):
        return self.reservas

    def crear_reserva(self, sala, usuario, fecha, hora):
        # Verifica si ya existe una reserva para la misma sala, fecha y hora
        for r in self.reservas:
            if r["sala"] == sala and r["fecha"] == fecha and r["hora"] == hora:
                # Lanza una excepción para que el formulario la capture
                raise Exception("La sala ya está reservada en ese horario.")
        reserva = {
            "id": len(self.reservas) + 1,
            "sala": sala,
            "usuario": usuario,
            "fecha": fecha,
            "hora": hora
        }
        self.reservas.append(reserva)
        self.notify_observers(event="reserva_creada", data=reserva)
        return reserva

    def eliminar_reserva(self, reserva_id):
        self.reservas = [r for r in self.reservas if r["id"] != reserva_id]
        self.notify_observers(event="reserva_eliminada", data=reserva_id)

    def contar_reservas(self):
        return len(self.reservas)

    def obtener_reservas_por_usuario(self, username):
        return [reserva for reserva in self.reservas if reserva["usuario"] == username]