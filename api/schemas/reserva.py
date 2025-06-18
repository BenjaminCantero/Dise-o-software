from pydantic import BaseModel, root_validator
from datetime import datetime

class ReservaIn(BaseModel):
    usuario_id: int
    sala_id: int
    fecha_inicio: datetime
    fecha_fin: datetime

    @root_validator
    def validate_fechas(cls, values):
        fecha_inicio = values.get("fecha_inicio")
        fecha_fin = values.get("fecha_fin")
        if fecha_inicio is None or fecha_fin is None:
            raise ValueError("Las fechas no pueden ser nulas")
        if fecha_inicio >= fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
        return values

class ReservaOut(ReservaIn):
    id: int

    class Config:
        orm_mode = True