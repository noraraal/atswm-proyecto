from backend.entities.base import Session
from backend.entities.reserva_entity import ReservaEntity


class ReservaRepo:

    def create(self, cliente_id, alojamiento_id, fecha_entrada,
               fecha_salida, num_huespedes, precio_total):
        session = Session()
        entity = ReservaEntity(
            cliente_id=cliente_id,
            alojamiento_id=alojamiento_id,
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            num_huespedes=num_huespedes,
            precio_total=precio_total,
            estado='confirmada'
        )
        session.add(entity)
        session.commit()
        rid = entity.id
        session.close()
        return rid

    def find_by_id(self, reserva_id):
        session = Session()
        entity = session.query(ReservaEntity).get(reserva_id)
        session.close()
        return entity

    def find_by_cliente(self, cliente_id):
        session = Session()
        entities = session.query(ReservaEntity).filter_by(
            cliente_id=cliente_id).all()
        session.close()
        return entities

    def find_all(self):
        session = Session()
        entities = session.query(ReservaEntity).all()
        session.close()
        return entities

    def has_active_for_alojamiento(self, alojamiento_id):
        session = Session()
        count = session.query(ReservaEntity).filter(
            ReservaEntity.alojamiento_id == alojamiento_id,
            ReservaEntity.estado.in_(['pendiente', 'confirmada'])
        ).count()
        session.close()
        return count > 0

    def check_disponibilidad(self, alojamiento_id, fecha_entrada, fecha_salida):
        """Devuelve True si el alojamiento esta disponible en esas fechas."""
        session = Session()
        conflictos = session.query(ReservaEntity).filter(
            ReservaEntity.alojamiento_id == alojamiento_id,
            ReservaEntity.estado.in_(['pendiente', 'confirmada']),
            ReservaEntity.fecha_entrada < fecha_salida,
            ReservaEntity.fecha_salida > fecha_entrada
        ).count()
        session.close()
        return conflictos == 0

    def update_estado(self, reserva_id, estado):
        session = Session()
        entity = session.query(ReservaEntity).get(reserva_id)
        if not entity:
            session.close()
            return False
        entity.estado = estado
        session.commit()
        session.close()
        return True

    def delete(self, reserva_id):
        session = Session()
        entity = session.query(ReservaEntity).get(reserva_id)
        if not entity:
            session.close()
            return False
        session.delete(entity)
        session.commit()
        session.close()
        return True
