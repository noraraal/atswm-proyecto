from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey
from datetime import datetime
from backend.entities.base import Base


class ReservaEntity(Base):
    __tablename__ = 'reservas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    alojamiento_id = Column(Integer, ForeignKey('alojamientos.id'), nullable=False)
    fecha_entrada = Column(Date, nullable=False)
    fecha_salida = Column(Date, nullable=False)
    num_huespedes = Column(Integer, nullable=False)
    precio_total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(15), nullable=False, default='confirmada')
    fecha_reserva = Column(DateTime, default=datetime.utcnow)
