from flask import Blueprint, request, jsonify
from backend.sessions import validate_session

alojamiento_bp = Blueprint('alojamientos', __name__)

app_instance = None


def _get_current_user():
    token = request.cookies.get('session')
    if not token:
        return None
    user_id = validate_session(token)
    if not user_id:
        return None
    return app_instance.get_user(user_id)


def _alojamiento_to_dict(a):
    return {
        'id': a.id,
        'titulo': a.titulo,
        'tipo': a.tipo,
        'ciudad': a.ciudad,
        'direccion': a.direccion,
        'precio_noche': float(a.precio_noche),
        'capacidad': a.capacidad,
        'descripcion': a.descripcion,
        'servicios': a.servicios,
        'imagen_url': a.imagen_url
    }


@alojamiento_bp.route('/alojamientos', methods=['GET'])
def list_alojamientos():
    ciudad = request.args.get('ciudad')
    tipo = request.args.get('tipo')
    huespedes = request.args.get('huespedes', type=int)

    alojamientos = app_instance.list_alojamientos(ciudad, tipo, huespedes)
    return jsonify([_alojamiento_to_dict(a) for a in alojamientos])


@alojamiento_bp.route('/alojamientos/<int:id>', methods=['GET'])
def get_alojamiento(id):
    alojamiento = app_instance.get_alojamiento(id)
    if not alojamiento:
        return jsonify({'error': 'Alojamiento no encontrado'}), 404
    return jsonify(_alojamiento_to_dict(alojamiento))


@alojamiento_bp.route('/alojamientos', methods=['POST'])
def create_alojamiento():
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401
    if user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado: se requiere rol admin'}), 403

    data = request.get_json()
    required = ['titulo', 'tipo', 'ciudad', 'precio_noche', 'capacidad']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Campo obligatorio: {field}'}), 400

    app_instance.create_alojamiento(
        titulo=data['titulo'],
        tipo=data['tipo'],
        ciudad=data['ciudad'],
        direccion=data.get('direccion'),
        precio_noche=data['precio_noche'],
        capacidad=data['capacidad'],
        descripcion=data.get('descripcion'),
        servicios=data.get('servicios'),
        imagen_url=data.get('imagen_url')
    )
    return jsonify({'message': 'Alojamiento creado correctamente'}), 201


@alojamiento_bp.route('/alojamientos/<int:id>', methods=['PUT'])
def update_alojamiento(id):
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401
    if user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado: se requiere rol admin'}), 403

    if not app_instance.get_alojamiento(id):
        return jsonify({'error': 'Alojamiento no encontrado'}), 404

    data = request.get_json()
    app_instance.update_alojamiento(
        id,
        titulo=data.get('titulo'),
        tipo=data.get('tipo'),
        ciudad=data.get('ciudad'),
        direccion=data.get('direccion'),
        precio_noche=data.get('precio_noche'),
        capacidad=data.get('capacidad'),
        descripcion=data.get('descripcion'),
        servicios=data.get('servicios'),
        imagen_url=data.get('imagen_url')
    )
    return jsonify({'message': 'Alojamiento actualizado correctamente'})


@alojamiento_bp.route('/alojamientos/<int:id>', methods=['DELETE'])
def delete_alojamiento(id):
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401
    if user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado: se requiere rol admin'}), 403

    if not app_instance.get_alojamiento(id):
        return jsonify({'error': 'Alojamiento no encontrado'}), 404

    try:
        app_instance.delete_alojamiento(id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
