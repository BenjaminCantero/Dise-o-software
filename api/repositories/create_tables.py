from api.db import engine
from api.db import Base

# Esto crea todas las tablas definidas en tus modelos
Base.metadata.create_all(bind=engine)