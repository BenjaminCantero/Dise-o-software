class ReservaService:
    def __init__(self):
        # Aquí puedes inicializar una lista de reservas o conectar con el repositorio
        self.reservas = []

    def listar_reservas(self):
        return self.reservas

    def crear_reserva(self, sala, usuario, fecha, hora):
        reserva = {
            "id": len(self.reservas) + 1,
            "sala": sala,
            "usuario": usuario,
            "fecha": fecha,
            "hora": hora
        }
        self.reservas.append(reserva)
        return reserva

    def eliminar_reserva(self, reserva_id):
        self.reservas = [r for r in self.reservas if r["id"] != reserva_id]

    def contar_reservas(self):
        return len(self.reservas)