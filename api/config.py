import os
from fastapi.middleware.cors import CORSMiddleware
import logging

# Variables de entorno y configuración global
API_TITLE = os.getenv("API_TITLE", "SmartRoom API")
API_VERSION = os.getenv("API_VERSION", "1.0.0")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Función para agregar CORS a la app

def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
