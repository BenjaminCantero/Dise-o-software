import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.db import SessionLocal
import api.models  # Importa todos los modelos para registrar relaciones
from api.models.usuario import Usuario

db = SessionLocal()

admin = Usuario(username="admin", password="admin123", role="admin")
estudiante = Usuario(username="estudiante", password="estudiante123", role="estudiante")
profesor = Usuario(username="profesor", password="profesor123", role="profesor")

db.add_all([admin, estudiante, profesor])
db.commit()

print("Usuarios de prueba creados exitosamente.")

db.close()