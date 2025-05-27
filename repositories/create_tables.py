from .db import engine
from .models import Base

# Esto crea todas las tablas definidas en tus modelos
Base.metadata.create_all(bind=engine)