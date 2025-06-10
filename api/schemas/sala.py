from pydantic import BaseModel, validator, model_validator
from datetime import datetime

class SalaIn(BaseModel):
    nombre: str
    capacidad: int
    estado: str = "disponible"

    @validator('capacidad')
    def validate_capacidad(cls, value):
        if value <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        return value

class SalaOut(SalaIn):
    id: int

class ReservaIn(BaseModel):
    sala_nombre: str
    usuario_username: str
    fecha_inicio: datetime
    fecha_fin: datetime

    @model_validator(mode="after")
    def validate_fechas(self):
        if self.fecha_inicio is None or self.fecha_fin is None:
            raise ValueError("Las fechas no pueden ser nulas")
        if self.fecha_inicio >= self.fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
        return self

class ReservaOut(ReservaIn):
    id: int