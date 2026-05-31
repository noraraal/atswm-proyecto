from backend.entities.base import Session
from backend.entities.alojamiento_entity import AlojamientoEntity


class AlojamientoRepo:

    def create(self, **kwargs):
        session = Session()
        entity = AlojamientoEntity(**kwargs)
        session.add(entity)
        session.commit()
        aid = entity.id
        session.close()
        return aid

    def find_by_id(self, alojamiento_id):
        session = Session()
        entity = session.query(AlojamientoEntity).get(alojamiento_id)
        session.close()
        return entity

    def find_all(self, ciudad=None, tipo=None, huespedes=None):
        session = Session()
        query = session.query(AlojamientoEntity)
        if ciudad:
            query = query.filter(AlojamientoEntity.ciudad.ilike(f"%{ciudad}%"))
        if tipo:
            query = query.filter_by(tipo=tipo)
        if huespedes:
            query = query.filter(AlojamientoEntity.capacidad >= huespedes)
        entities = query.all()
        session.close()
        return entities

    def update(self, alojamiento_id, **kwargs):
        session = Session()
        entity = session.query(AlojamientoEntity).get(alojamiento_id)
        if not entity:
            session.close()
            return False
        for key, value in kwargs.items():
            if hasattr(entity, key) and value is not None:
                setattr(entity, key, value)
        session.commit()
        session.close()
        return True

    def delete(self, alojamiento_id):
        session = Session()
        entity = session.query(AlojamientoEntity).get(alojamiento_id)
        if not entity:
            session.close()
            return False
        session.delete(entity)
        session.commit()
        session.close()
        return True
