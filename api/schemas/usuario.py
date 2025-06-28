from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class RolEnum(str, Enum):
    admin = "admin"
    profesor = "profesor"
    estudiante = "estudiante"

class UsuarioIn(BaseModel):
    username: str
    password: str
    role: RolEnum

class UsuarioUpdate(BaseModel):
    username: str
    role: RolEnum

class UsuarioOut(BaseModel):
    id: int
    username: str
    role: RolEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True