from fastapi import APIRouter
from services.user_service import UserService
from api.schemas.usuario import UserIn, UserEdit, UserOut  # Import corregido

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
user_service = UserService()

@router.get("/", response_model=list[UserOut])
def get_usuarios():
    usuarios = user_service.listar_usuarios()
    return [{"username": u.username, "role": u.role} for u in usuarios]

@router.post("/", response_model=UserOut, status_code=201)
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

@router.put("/{username}")
def update_usuario(username: str, usuario: UserEdit):
    user_service.editar_usuario(username=username, role=usuario.role)
    return {"message": "Usuario actualizado correctamente"}

@router.delete("/{username}")
def delete_usuario(username: str):
    user_service.eliminar_usuario(username)
    return {"message": "Usuario eliminado correctamente"}