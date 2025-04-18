from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Sala(Base):
    __tablename__ = "salas"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    capacidad = Column(Integer)
    estado = Column(String)

    reservas = relationship("Reserva", back_populates="sala")

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True)
    responsable = Column(String)
    fecha = Column(String)  # o Date si quieres manejar fechas
    hora = Column(String)   # o Time si es una sola hora
    estado = Column(String)

    sala_id = Column(Integer, ForeignKey("salas.id"))
    sala = relationship("Sala", back_populates="reservas")
