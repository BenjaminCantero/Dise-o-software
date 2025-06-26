from pydantic import BaseModel, model_validator
from datetime import datetime

class ReservaIn(BaseModel):
    usuario_id: int
    sala_id: int
    fecha_inicio: datetime
    fecha_fin: datetime

    @model_validator(mode="after")
    def check_fechas(self):
        if self.fecha_inicio is None or self.fecha_fin is None:
            raise ValueError("Las fechas no pueden ser nulas")
        if self.fecha_inicio >= self.fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin.")
        return self

class ReservaOut(ReservaIn):
    id: int

    class Config:
        from_attributes = True