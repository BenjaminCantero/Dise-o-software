from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base

class Sala(Base):
    __tablename__ = "salas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    capacidad = Column(Integer, nullable=False)
    estado = Column(String, nullable=False, default="disponible")

    reservas = relationship("Reserva", back_populates="sala")