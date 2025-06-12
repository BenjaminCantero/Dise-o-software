from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from api.db import SessionLocal
from api.models import Sala
from api.schemas.sala import SalaIn, SalaOut

router = APIRouter(prefix="/salas", tags=["salas"])

def adapt_sala(sala: Sala):
    return SalaOut(
        id=sala.id,
        nombre=sala.nombre,
        capacidad=sala.capacidad,
        estado=sala.estado
    )

@router.get("/", response_model=list[SalaOut])
def get_salas():
    db = SessionLocal()
    try:
        salas = db.query(Sala).all()
        return [adapt_sala(s) for s in salas]
    finally:
        db.close()

@router.get("/{sala_id}", response_model=SalaOut)
def get_sala(sala_id: int):
    db = SessionLocal()
    try:
        sala = db.query(Sala).filter_by(id=sala_id).first()
        if not sala:
            raise HTTPException(status_code=404, detail="Sala no encontrada")
        return adapt_sala(sala)
    finally:
        db.close()

@router.post("/", response_model=SalaOut, status_code=201)
def create_sala(sala: SalaIn):
    db = SessionLocal()
    try:
        existente = db.query(Sala).filter_by(nombre=sala.nombre).first()
        if existente:
            raise HTTPException(status_code=400, detail="Ya existe una sala con ese nombre")
        if sala.estado.lower() not in ["ocupada", "disponible"]:
            raise HTTPException(status_code=400, detail="Agregue un estado válido: 'ocupada' o 'disponible'")
        nueva = Sala(
            nombre=sala.nombre,
            capacidad=sala.capacidad,
            estado=sala.estado.lower()
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return adapt_sala(nueva)
    finally:
        db.close()

@router.put("/{sala_id}", response_model=SalaOut)
def update_sala(sala_id: int, sala: SalaIn):
    db = SessionLocal()
    try:
        sala_db = db.query(Sala).filter_by(id=sala_id).first()
        if not sala_db:
            raise HTTPException(status_code=404, detail="Sala no encontrada")
        if sala_db.nombre != sala.nombre:
            existente = db.query(Sala).filter_by(nombre=sala.nombre).first()
            if existente:
                raise HTTPException(status_code=400, detail="Ya existe una sala con ese nombre")
        if sala.estado.lower() not in ["ocupada", "disponible"]:
            raise HTTPException(status_code=400, detail="Agregue un estado válido: 'ocupada' o 'disponible'")
        sala_db.nombre = sala.nombre
        sala_db.capacidad = sala.capacidad
        sala_db.estado = sala.estado.lower()
        db.commit()
        db.refresh(sala_db)
        return adapt_sala(sala_db)
    finally:
        db.close()

@router.delete("/{sala_id}", response_model=list[SalaOut])
def delete_sala(sala_id: int):
    db = SessionLocal()
    try:
        sala = db.query(Sala).filter_by(id=sala_id).first()
        if not sala:
            raise HTTPException(status_code=404, detail="Sala no encontrada")
        db.delete(sala)
        db.commit()
        salas = db.query(Sala).all()
        return [adapt_sala(s) for s in salas]
    finally:
        db.close()