from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base, TimestampMixin

class Usuario(Base, TimestampMixin):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    reservas = relationship("Reserva", back_populates="usuario")