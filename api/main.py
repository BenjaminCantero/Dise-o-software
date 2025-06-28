from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .db import Base, engine
from .routes.reservas import router as reservas_router
from .routes.usuarios import router as usuarios_router
from .routes.salas import router as salas_router
from .routes.login import router as login_router
from .config import add_cors, API_TITLE, API_VERSION

app = FastAPI(title=API_TITLE, version=API_VERSION)

add_cors(app)

Base.metadata.create_all(bind=engine)

# Manejo global de errores
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

app.include_router(reservas_router)
app.include_router(usuarios_router)
app.include_router(salas_router)
app.include_router(login_router)