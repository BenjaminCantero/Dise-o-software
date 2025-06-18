from pydantic import BaseModel
from enum import Enum

class RolEnum(str, Enum):
    admin = "admin"
    estudiante = "estudiante"
    profesor = "profesor"

class UsuarioIn(BaseModel):
    username: str
    password: str
    role: RolEnum  # Solo acepta estos valores

class UsuarioOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True