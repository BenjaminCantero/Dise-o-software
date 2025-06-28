from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import DateTime, func, Column  # Se agrega Column aquí

DATABASE_URL = "sqlite:///./api.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Clase base con timestamps de auditoría
class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)