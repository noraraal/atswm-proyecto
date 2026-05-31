from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.entities.base import Base


class UsuarioEntity(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(10), nullable=False, default='cliente')
    fecha_alta = Column(DateTime, default=datetime.utcnow)
