from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.sala import SalaIn, SalaOut
from ..services.sala_service import SalaService
from ..db import SessionLocal

router = APIRouter(prefix="/salas", tags=["salas"])

sala_service = SalaService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[SalaOut])
def listar_salas(db: Session = Depends(get_db)):
    salas = sala_service.listar_salas(db)
    return [SalaOut.from_orm(s) for s in salas]

@router.get("/{sala_id}", response_model=SalaOut)
def get_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = sala_service.obtener_sala_por_id(db, sala_id)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return SalaOut.from_orm(sala)

@router.post("/", response_model=SalaOut, status_code=201)
def create_sala(sala: SalaIn, db: Session = Depends(get_db)):
    try:
        nueva_sala = sala_service.crear_sala(db, sala.nombre, sala.capacidad, sala.estado)
        return SalaOut.from_orm(nueva_sala)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{sala_id}", response_model=SalaOut)
def update_sala(sala_id: int, sala: SalaIn, db: Session = Depends(get_db)):
    try:
        sala_actualizada = sala_service.editar_sala(db, sala_id, sala.nombre, sala.capacidad, sala.estado)
        return SalaOut.from_orm(sala_actualizada)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{sala_id}", response_model=list[SalaOut])
def delete_sala(sala_id: int, db: Session = Depends(get_db)):
    sala_service.eliminar_sala(db, sala_id)
    salas = sala_service.listar_salas(db)
    return [SalaOut.from_orm(s) for s in salas]