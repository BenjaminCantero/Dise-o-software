from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    sala_id = Column(Integer, ForeignKey("salas.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    sala = relationship("Sala", back_populates="reservas")
    usuario = relationship("Usuario")