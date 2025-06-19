from fastapi import FastAPI
from .db import Base, engine
from .routes.reservas import router as reservas_router
from .routes.usuarios import router as usuarios_router
from .routes.salas import router as salas_router
from .routes.login import router as login_router  # <-- Agrega esta línea

app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(reservas_router)
app.include_router(usuarios_router)
app.include_router(salas_router)
app.include_router(login_router)  # <-- Agrega esta línea