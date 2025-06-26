from pydantic import BaseModel, Field
from enum import Enum

class EstadoSalaEnum(str, Enum):
    disponible = "disponible"
    ocupada = "ocupada"

class SalaIn(BaseModel):
    nombre: str
    capacidad: int = Field(..., gt=0, description="La capacidad debe ser mayor a 0")
    estado: EstadoSalaEnum  # Solo acepta estos valores

class SalaOut(SalaIn):
    id: int

    class Config:
        
        from_attributes = True