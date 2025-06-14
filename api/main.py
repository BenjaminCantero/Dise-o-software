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

@app.get("/salas", response_model=list[SalaOut])
def get_salas():
    return sala_service.listar_salas()

@app.post("/salas", response_model=SalaOut, status_code=201)
def create_sala(sala: SalaIn):
    nueva = sala_service.crear_sala(
        nombre=sala.nombre,
        capacidad=sala.capacidad,
        estado=sala.estado
    )
    return nueva

@app.put("/salas/{sala_id}")
def update_sala(sala_id: int, sala: SalaIn):
    salas = sala_service.listar_salas()
    if not any(getattr(s, "id", s.get("id")) == sala_id for s in salas):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    sala_service.editar_sala(
        sala_id=sala_id,
        nombre=sala.nombre,
        capacidad=sala.capacidad,
        estado=sala.estado
    )
    return {"message": "Sala actualizada correctamente"}

@app.delete("/salas/{sala_id}")
def delete_sala(sala_id: int):
    salas = sala_service.listar_salas()
    if not any(getattr(s, "id", s.get("id")) == sala_id for s in salas):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    sala_service.eliminar_sala(sala_id)
    return {"message": "Sala eliminada correctamente"}

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

@app.get("/reservas", response_model=list[ReservaOut])
def get_reservas():
    return reserva_service.listar_reservas()

@app.get("/reservas/{reserva_id}", response_model=ReservaOut)
def get_reserva(reserva_id: int):
    reserva = reserva_service.obtener_reserva_por_id(reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@app.post("/reservas", response_model=ReservaOut, status_code=201)
def create_reserva(reserva: ReservaIn):
    salas = sala_service.listar_salas()
    if not any(getattr(s, "nombre", s.get("nombre")) == reserva.sala_nombre for s in salas):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    usuarios = user_service.listar_usuarios()
    if not any(getattr(u, "username", u.get("username")) == reserva.usuario_username for u in usuarios):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    try:
        nueva = reserva_service.crear_reserva(
            sala_nombre=reserva.sala_nombre,
            usuario_username=reserva.usuario_username,
            fecha_inicio=reserva.fecha_inicio,
            fecha_fin=reserva.fecha_fin
        )
        return nueva
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.put("/reservas/{reserva_id}")
def update_reserva(reserva_id: int, reserva: ReservaIn):
    try:
        reserva_service.editar_reserva(
            reserva_id=reserva_id,
            sala_nombre=reserva.sala_nombre,
            usuario_username=reserva.usuario_username,
            fecha_inicio=reserva.fecha_inicio,
            fecha_fin=reserva.fecha_fin
        )
        return {"message": "Reserva actualizada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.delete("/reservas/{reserva_id}")
def delete_reserva(reserva_id: int):
    try:
        reserva_service.eliminar_reserva(reserva_id)
        return {"message": "Reserva eliminada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

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

@app.get("/usuarios", response_model=list[UserOut])
def get_usuarios():
    usuarios = user_service.listar_usuarios()
    return [{"username": u.username, "role": u.role} for u in usuarios]

@app.post("/usuarios", response_model=UserOut, status_code=201)
def create_usuario(usuario: UserIn):
    nuevo = user_service.crear_usuario(
        username=usuario.username,
        password=usuario.password,
        role=usuario.role
    )
    return {
        "username": nuevo.username,
        "role": nuevo.role
    }

@app.put("/usuarios/{username}")
def update_usuario(username: str, usuario: UserEdit):
    user_service.editar_usuario(username=username, role=usuario.role)
    return {"message": "Usuario actualizado correctamente"}

@app.delete("/usuarios/{username}")
def delete_usuario(username: str):
    user_service.eliminar_usuario(username)
    return {"message": "Usuario eliminado correctamente"}