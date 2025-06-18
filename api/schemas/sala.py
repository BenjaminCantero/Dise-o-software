from pydantic import BaseModel

class SalaIn(BaseModel):
    nombre: str
    capacidad: int
    estado: str

class SalaOut(SalaIn):
    id: int

    class Config:
        orm_mode = True