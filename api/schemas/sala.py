from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class EstadoSalaEnum(str, Enum):
    disponible = "disponible"
    ocupada = "ocupada"

class SalaIn(BaseModel):
    nombre: str
    capacidad: int = Field(..., gt=0, description="La capacidad debe ser mayor a 0")
    estado: EstadoSalaEnum  # Solo acepta estos valores

class SalaOut(SalaIn):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        
        from_attributes = True