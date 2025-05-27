from .db import SessionLocal
from .models import Usuario

db = SessionLocal()

admin = Usuario(username="admin", password="admin123", role="admin")
estudiante = Usuario(username="estudiante", password="estudiante123", role="estudiante")
profesor = Usuario(username="profesor", password="profesor123", role="profesor")

db.add_all([admin, estudiante, profesor])
db.commit()

print("Usuarios de prueba creados exitosamente.")

db.close()