from repositories.db import SessionLocal
from repositories.models import Usuario

db = SessionLocal()
for u in db.query(Usuario).all():
    print(u.username, u.password)
db.close()