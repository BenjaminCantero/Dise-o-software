from pydantic import BaseModel, validator, root_validator
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

    @root_validator(pre=True)
    def validate_fechas(cls, values):
        fecha_inicio = values.get('fecha_inicio')
        fecha_fin = values.get('fecha_fin')
        if fecha_inicio is None or fecha_fin is None:
            raise ValueError("Las fechas no pueden ser nulas")
        if fecha_inicio >= fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
        return values

class ReservaOut(ReservaIn):
    id: int