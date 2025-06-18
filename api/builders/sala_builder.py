from api.repositories.sala_repository import Sala

class SalaBuilder:
    def __init__(self):
        self._nombre = None
        self._capacidad = None
        self._estado = None

    def set_nombre(self, nombre):
        self._nombre = nombre
        return self

    def set_capacidad(self, capacidad):
        self._capacidad = capacidad
        return self

    def set_estado(self, estado):
        self._estado = estado
        return self

    def build(self):
        if self._nombre is None:
            raise ValueError("El nombre de la sala es obligatorio")
        if self._capacidad is None:
            raise ValueError("La capacidad de la sala es obligatoria")
        if self._estado is None:
            raise ValueError("El estado de la sala es obligatorio")
        
        return Sala(
            nombre=self._nombre,
            capacidad=self._capacidad,
            estado=self._estado
        )
