import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.db import SessionLocal
import api.models  # Importa todos los modelos para registrar relaciones
from api.models.sala import Sala

db = SessionLocal()

salas = [
    Sala(nombre="CJP", capacidad=30, estado="disponible"),
    Sala(nombre="CFT", capacidad=25, estado="disponible"),
    Sala(nombre="LAB1", capacidad=20, estado="ocupada"),
    Sala(nombre="AULA101", capacidad=40, estado="disponible"),
]

db.add_all(salas)
db.commit()

print("Salas de prueba creadas exitosamente.")

db.close()
