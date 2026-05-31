from backend.entities.base import Session
from backend.entities.usuario_entity import UsuarioEntity


class UsuarioRepo:

    def create(self, nombre, email, password_hash):
        session = Session()
        entity = UsuarioEntity(
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            rol='cliente'
        )
        session.add(entity)
        session.commit()
        uid = entity.id
        session.close()
        return uid

    def find_by_email(self, email):
        session = Session()
        entity = session.query(UsuarioEntity).filter_by(email=email).first()
        session.close()
        return entity

    def find_by_id(self, user_id):
        session = Session()
        entity = session.query(UsuarioEntity).get(user_id)
        session.close()
        return entity

    def find_all(self):
        session = Session()
        entities = session.query(UsuarioEntity).all()
        session.close()
        return entities

    def update(self, user_id, **kwargs):
        session = Session()
        entity = session.query(UsuarioEntity).get(user_id)
        if not entity:
            session.close()
            return False
        for key, value in kwargs.items():
            if hasattr(entity, key) and value is not None:
                setattr(entity, key, value)
        session.commit()
        session.close()
        return True

    def delete(self, user_id):
        session = Session()
        entity = session.query(UsuarioEntity).get(user_id)
        if not entity:
            session.close()
            return False
        session.delete(entity)
        session.commit()
        session.close()
        return True
