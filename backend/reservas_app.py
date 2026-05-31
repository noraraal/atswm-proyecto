from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from backend.repositories.usuario_repo import UsuarioRepo
from backend.repositories.alojamiento_repo import AlojamientoRepo
from backend.repositories.reserva_repo import ReservaRepo


class ReservasApp:
    """Clase principal de logica de negocio (equivalente a BookTrack)."""

    def __init__(self):
        self.usuario_repo = UsuarioRepo()
        self.alojamiento_repo = AlojamientoRepo()
        self.reserva_repo = ReservaRepo()

    # --- Auth ---

    def register_user(self, nombre, email, password):
        if self.usuario_repo.find_by_email(email):
            raise ValueError("El email ya esta registrado")
        hashed = generate_password_hash(password)
        return self.usuario_repo.create(nombre, email, hashed)

    def validate_credentials(self, email, password):
        """Devuelve el entity del usuario si las credenciales son correctas."""
        user = self.usuario_repo.find_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    # --- Usuarios ---

    def get_user(self, user_id):
        return self.usuario_repo.find_by_id(user_id)

    def list_users(self):
        return self.usuario_repo.find_all()

    def update_user(self, user_id, **kwargs):
        # Si viene password, hashearlo
        if 'password' in kwargs and kwargs['password']:
            kwargs['password_hash'] = generate_password_hash(kwargs.pop('password'))
        else:
            kwargs.pop('password', None)
        # Verificar email unico
        if 'email' in kwargs and kwargs['email']:
            existing = self.usuario_repo.find_by_email(kwargs['email'])
            if existing and existing.id != user_id:
                raise ValueError("El email ya esta en uso")
        return self.usuario_repo.update(user_id, **kwargs)

    def delete_user(self, user_id):
        return self.usuario_repo.delete(user_id)

    # --- Alojamientos ---

    def list_alojamientos(self, ciudad=None, tipo=None, huespedes=None):
        return self.alojamiento_repo.find_all(ciudad, tipo, huespedes)

    def get_alojamiento(self, alojamiento_id):
        return self.alojamiento_repo.find_by_id(alojamiento_id)

    def create_alojamiento(self, **kwargs):
        return self.alojamiento_repo.create(**kwargs)

    def update_alojamiento(self, alojamiento_id, **kwargs):
        return self.alojamiento_repo.update(alojamiento_id, **kwargs)

    def check_disponibilidad(self, alojamiento_id, fecha_entrada, fecha_salida):
        return self.reserva_repo.check_disponibilidad(
            alojamiento_id, fecha_entrada, fecha_salida)

    def delete_alojamiento(self, alojamiento_id):
        if self.reserva_repo.has_active_for_alojamiento(alojamiento_id):
            raise ValueError("Tiene reservas activas asociadas")
        return self.alojamiento_repo.delete(alojamiento_id)

    # --- Reservas ---

    def create_reserva(self, cliente_id, alojamiento_id, fecha_entrada,
                       fecha_salida, num_huespedes):
        alojamiento = self.alojamiento_repo.find_by_id(alojamiento_id)
        if not alojamiento:
            raise ValueError("Alojamiento no encontrado")
        if num_huespedes > alojamiento.capacidad:
            raise ValueError("Numero de huespedes supera la capacidad")
        if fecha_entrada >= fecha_salida:
            raise ValueError("La fecha de entrada debe ser anterior a la de salida")
        if fecha_entrada < date.today():
            raise ValueError("La fecha de entrada debe ser futura")
        if not self.reserva_repo.check_disponibilidad(
                alojamiento_id, fecha_entrada, fecha_salida):
            raise ValueError("Alojamiento no disponible en esas fechas")

        noches = (fecha_salida - fecha_entrada).days
        precio_total = float(alojamiento.precio_noche) * noches

        reserva_id = self.reserva_repo.create(
            cliente_id, alojamiento_id, fecha_entrada,
            fecha_salida, num_huespedes, precio_total
        )
        return reserva_id, precio_total

    def list_reservas(self, cliente_id=None):
        if cliente_id:
            return self.reserva_repo.find_by_cliente(cliente_id)
        return self.reserva_repo.find_all()

    def get_reserva(self, reserva_id):
        return self.reserva_repo.find_by_id(reserva_id)

    def update_reserva_estado(self, reserva_id, estado):
        if estado not in ('pendiente', 'confirmada', 'cancelada'):
            raise ValueError("Estado invalido")
        return self.reserva_repo.update_estado(reserva_id, estado)

    def delete_reserva(self, reserva_id):
        return self.reserva_repo.delete(reserva_id)
