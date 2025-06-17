from pydantic import BaseModel

class UsuarioIn(BaseModel):
    username: str
    password: str
    role: str

class UsuarioOut(BaseModel):
    id: int
    username: str
    role: str