from fastapi import FastAPI
from .db import Base, engine
from .routes.reservas import router as reservas_router
from .routes.usuarios import router as usuarios_router
from .routes.salas import router as salas_router
from .middleware.logging import LoggingMiddleware
from .middleware.errores import ErrorHandlingMiddleware
from .middleware.header import CustomHeaderMiddleware
from .middleware.autenticacion import AuthMiddleware

app = FastAPI()

app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(CustomHeaderMiddleware)
app.add_middleware(AuthMiddleware)  

Base.metadata.create_all(bind=engine)

app.include_router(reservas_router)
app.include_router(usuarios_router)
app.include_router(salas_router)