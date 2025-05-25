from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .db import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="usuario")  # <--- Agrega esta línea
    reservas = relationship("Reserva", back_populates="usuario")

class Sala(Base):
    __tablename__ = "salas"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    capacidad = Column(Integer, nullable=False)
    reservas = relationship("Reserva", back_populates="sala")

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="reservas")
    sala_id = Column(Integer, ForeignKey("salas.id"))
    sala = relationship("Sala", back_populates="reservas")