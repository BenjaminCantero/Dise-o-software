class Mediator:
    def __init__(self):
        self.componentes = {}

    def registrar(self, nombre, componente):
        self.componentes[nombre] = componente

    def notificar(self, evento, datos=None):
        # Puedes personalizar los eventos según tus necesidades
        if evento == "sala_actualizada":
            if "inicio" in self.componentes:
                self.componentes["inicio"].actualizar()
            if "reservas" in self.componentes:
                self.componentes["reservas"].actualizar()
        elif evento == "reserva_realizada":
            if "reportes" in self.componentes:
                self.componentes["reportes"].actualizar()
        # Agrega más eventos según lo requiera tu sistema