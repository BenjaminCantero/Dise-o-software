import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator, model_validator
from typing import Optional
from datetime import datetime
from services.sala_service import SalaService
from services.reserva_service import ReservaService
from services.user_service import UserService
from api.routes.salas import router as salas_router
from api.routes.reservas import router as reservas_router
from api.routes.usuarios import router as usuarios_router

app = FastAPI()
sala_service = SalaService()
reserva_service = ReservaService()
user_service = UserService()

# Esquema para crear/editar sala
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

@app.get("/")
def read_root():
    return {"message": "API de Diseño de Software funcionando"}

app.include_router(salas_router)
app.include_router(reservas_router)
app.include_router(usuarios_router)

# Esquema para crear/editar reserva
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

# Esquema para crear/editar usuario
class UserIn(BaseModel):
    username: str
    password: str
    role: str

class UserEdit(BaseModel):
    role: str

class UserOut(BaseModel):
    username: str
    role: str