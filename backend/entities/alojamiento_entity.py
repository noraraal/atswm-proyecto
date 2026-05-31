from sqlalchemy import Column, Integer, String, Text, Numeric
from backend.entities.base import Base


class AlojamientoEntity(Base):
    __tablename__ = 'alojamientos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    tipo = Column(String(20), nullable=False)
    ciudad = Column(String(100), nullable=False)
    direccion = Column(String(255))
    precio_noche = Column(Numeric(8, 2), nullable=False)
    capacidad = Column(Integer, nullable=False)
    descripcion = Column(Text)
    servicios = Column(String(255))
    imagen_url = Column(String(255))
