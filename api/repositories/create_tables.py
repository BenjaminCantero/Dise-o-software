from api.db import engine
from api.models.usuario import Usuario
from api.models.sala import Sala
from api.models.reserva import Reserva
from api.db import Base

# Esto crea todas las tablas definidas en tus modelos
Base.metadata.create_all(bind=engine)