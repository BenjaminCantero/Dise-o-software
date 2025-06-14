from fastapi import APIRouter, HTTPException
from services.user_service import UserService
from api.schemas.usuario import UserIn, UserEdit, UserOut  # Import corregido
from services.reserva_service import ReservaService

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
user_service = UserService()
reserva_service = ReservaService()
ROLES_VALIDOS = {"admin", "profesor", "estudiante"}

@router.get("/", response_model=list[UserOut])
def get_usuarios():
    usuarios = user_service.listar_usuarios()
    return [{"username": u.username, "role": u.role} for u in usuarios]

@router.post("/", response_model=UserOut, status_code=201)
def create_usuario(usuario: UserIn):
    usuarios = user_service.listar_usuarios()
    if any(u.username == usuario.username for u in usuarios):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    if usuario.role not in ROLES_VALIDOS:
        raise HTTPException(status_code=400, detail="Agregue un rol válido: admin, profesor o estudiante")
    if not usuario.password or usuario.password.strip() == "":
        raise HTTPException(status_code=400, detail="La contraseña no puede estar vacía")
    nuevo = user_service.crear_usuario(
        username=usuario.username,
        password=usuario.password,
        role=usuario.role
    )
    return {
        "username": nuevo.username,
        "role": nuevo.role
    }


@router.put("/{username}", response_model=list[UserOut])
def update_usuario(username: str, usuario: UserEdit):
    usuarios = user_service.listar_usuarios()
    if not any(u.username == username for u in usuarios):
        raise HTTPException(status_code=404, detail="Nombre de usuario no válido")
    if usuario.role not in ROLES_VALIDOS:
        raise HTTPException(status_code=400, detail="Agregue un rol válido: admin, profesor o estudiante")
    user_service.editar_usuario(username=username, role=usuario.role)
    usuarios = user_service.listar_usuarios()
    return [{"username": u.username, "role": u.role} for u in usuarios]

@router.delete("/{username}", response_model=list[UserOut])
def delete_usuario(username: str):
    usuarios = user_service.listar_usuarios()
    if not any(u.username == username for u in usuarios):
        raise HTTPException(status_code=404, detail="Nombre de usuario no válido")
    # Eliminar reservas asociadas antes de eliminar el usuario
    reserva_service.eliminar_reservas_por_usuario(username)
    user_service.eliminar_usuario(username)
    usuarios = user_service.listar_usuarios()
    return [{"username": u.username, "role": u.role} for u in usuarios]