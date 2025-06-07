from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from services.sala_service import SalaService
from services.reserva_service import ReservaService
from services.user_service import UserService

app = FastAPI()
sala_service = SalaService()
reserva_service = ReservaService()
user_service = UserService()

# Esquema para crear/editar sala
class SalaIn(BaseModel):
    nombre: str
    capacidad: int
    estado: str = "disponible"

@app.get("/")
def read_root():
    return {"message": "API de Diseño de Software funcionando"}

@app.get("/salas")
def get_salas():
    return {"salas": sala_service.listar_salas()}

@app.post("/salas")
def create_sala(sala: SalaIn):
    nueva = sala_service.crear_sala(
        nombre=sala.nombre,
        capacidad=sala.capacidad,
        estado=sala.estado
    )
    return {
        "id": nueva.id,
        "nombre": nueva.nombre,
        "capacidad": nueva.capacidad,
        "estado": nueva.estado
    }

@app.put("/salas/{sala_id}")
def update_sala(sala_id: int, sala: SalaIn):
    # Verifica si la sala existe
    salas = sala_service.listar_salas()
    if not any(s["id"] == sala_id for s in salas):
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
    if not any(s["id"] == sala_id for s in salas):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    sala_service.eliminar_sala(sala_id)
    return {"message": "Sala eliminada correctamente"}

# Esquema para crear/editar reserva
class ReservaIn(BaseModel):
    sala_nombre: str
    usuario_username: str
    fecha_inicio: datetime
    fecha_fin: datetime

@app.get("/reservas")
def get_reservas():
    return {"reservas": reserva_service.listar_reservas()}

@app.get("/reservas/{reserva_id}")
def get_reserva(reserva_id: int):
    reserva = reserva_service.obtener_reserva_por_id(reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@app.post("/reservas")
def create_reserva(reserva: ReservaIn):
    try:
        nueva = reserva_service.crear_reserva(
            sala_nombre=reserva.sala_nombre,
            usuario_username=reserva.usuario_username,
            fecha_inicio=reserva.fecha_inicio,
            fecha_fin=reserva.fecha_fin
        )
        return {"id": nueva.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/reservas/{reserva_id}")
def delete_reserva(reserva_id: int):
    try:
        reserva_service.eliminar_reserva(reserva_id)
        return {"message": "Reserva eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Esquema para crear/editar usuario
class UserIn(BaseModel):
    username: str
    password: str
    role: str

class UserEdit(BaseModel):
    role: str

@app.get("/usuarios")
def get_usuarios():
    usuarios = user_service.listar_usuarios()
    return {"usuarios": [{"username": u.username, "role": u.role} for u in usuarios]}

@app.post("/usuarios")
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