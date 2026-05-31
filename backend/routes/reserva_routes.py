from datetime import datetime
from flask import Blueprint, request, jsonify
from backend.sessions import validate_session

reserva_bp = Blueprint('reservas', __name__)

app_instance = None


def _get_current_user():
    token = request.cookies.get('session')
    if not token:
        return None
    user_id = validate_session(token)
    if not user_id:
        return None
    return app_instance.get_user(user_id)


def _reserva_to_dict(r):
    return {
        'id': r.id,
        'cliente_id': r.cliente_id,
        'alojamiento_id': r.alojamiento_id,
        'fecha_entrada': r.fecha_entrada.isoformat(),
        'fecha_salida': r.fecha_salida.isoformat(),
        'num_huespedes': r.num_huespedes,
        'precio_total': float(r.precio_total),
        'estado': r.estado,
        'fecha_reserva': r.fecha_reserva.isoformat() if r.fecha_reserva else None
    }


@reserva_bp.route('/reservas', methods=['POST'])
def create_reserva():
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401

    data = request.get_json()
    required = ['alojamiento_id', 'fecha_entrada', 'fecha_salida', 'num_huespedes']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Campo obligatorio: {field}'}), 400

    try:
        fecha_entrada = datetime.strptime(data['fecha_entrada'], '%Y-%m-%d').date()
        fecha_salida = datetime.strptime(data['fecha_salida'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de fecha invalido (YYYY-MM-DD)'}), 400

    try:
        reserva_id, precio_total = app_instance.create_reserva(
            cliente_id=user.id,
            alojamiento_id=data['alojamiento_id'],
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            num_huespedes=data['num_huespedes']
        )
        return jsonify({
            'message': 'Reserva creada correctamente',
            'precio_total': precio_total
        }), 201
    except ValueError as e:
        error_msg = str(e)
        if 'no encontrado' in error_msg:
            return jsonify({'error': error_msg}), 404
        if 'no disponible' in error_msg:
            return jsonify({'error': error_msg}), 409
        return jsonify({'error': error_msg}), 400


@reserva_bp.route('/reservas', methods=['GET'])
def list_reservas():
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401

    if user.rol == 'admin':
        reservas = app_instance.list_reservas()
    else:
        reservas = app_instance.list_reservas(cliente_id=user.id)

    return jsonify([_reserva_to_dict(r) for r in reservas])


@reserva_bp.route('/reservas/<int:id>', methods=['GET'])
def get_reserva(id):
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401

    reserva = app_instance.get_reserva(id)
    if not reserva:
        return jsonify({'error': 'Reserva no encontrada'}), 404

    if user.rol != 'admin' and reserva.cliente_id != user.id:
        return jsonify({'error': 'La reserva pertenece a otro usuario'}), 403

    return jsonify(_reserva_to_dict(reserva))


@reserva_bp.route('/reservas/<int:id>', methods=['PATCH'])
def update_reserva(id):
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401

    reserva = app_instance.get_reserva(id)
    if not reserva:
        return jsonify({'error': 'Reserva no encontrada'}), 404

    data = request.get_json()
    estado = data.get('estado')

    if not estado:
        return jsonify({'error': 'Campo obligatorio: estado'}), 400

    # Cliente: solo puede cancelar sus propias reservas
    if user.rol != 'admin':
        if reserva.cliente_id != user.id:
            return jsonify({'error': 'El cliente solo puede cancelar sus propias reservas'}), 403
        if estado != 'cancelada':
            return jsonify({'error': 'El cliente solo puede cancelar reservas'}), 403
        if reserva.estado == 'cancelada':
            return jsonify({'error': 'La reserva ya esta cancelada'}), 409
        from datetime import date
        if reserva.fecha_entrada <= date.today():
            return jsonify({'error': 'No se puede cancelar: la fecha ya paso'}), 409

    try:
        app_instance.update_reserva_estado(id, estado)
        return jsonify({'message': 'Estado de la reserva actualizado'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@reserva_bp.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401
    if user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado: se requiere rol admin'}), 403

    if not app_instance.get_reserva(id):
        return jsonify({'error': 'Reserva no encontrada'}), 404

    app_instance.delete_reserva(id)
    return '', 204
