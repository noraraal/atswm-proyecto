from flask import Blueprint, request, jsonify
from backend.sessions import validate_session

usuario_bp = Blueprint('usuarios', __name__)

app_instance = None


def _get_current_user():
    """Obtiene el usuario autenticado a partir de la cookie."""
    token = request.cookies.get('session')
    if not token:
        return None
    user_id = validate_session(token)
    if not user_id:
        return None
    return app_instance.get_user(user_id)


def _user_to_dict(u):
    return {
        'id': u.id,
        'nombre': u.nombre,
        'email': u.email,
        'rol': u.rol,
        'fecha_alta': u.fecha_alta.isoformat() if u.fecha_alta else None
    }


@usuario_bp.route('/usuarios/me', methods=['GET'])
def get_me():
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401
    return jsonify(_user_to_dict(user))


@usuario_bp.route('/usuarios/me', methods=['PUT'])
def update_me():
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401

    data = request.get_json()
    try:
        app_instance.update_user(
            user.id,
            nombre=data.get('nombre'),
            email=data.get('email'),
            password=data.get('password')
        )
        return jsonify({'message': 'Perfil actualizado correctamente'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 409


@usuario_bp.route('/usuarios', methods=['GET'])
def list_usuarios():
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401
    if user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado: se requiere rol admin'}), 403

    usuarios = app_instance.list_users()
    return jsonify([_user_to_dict(u) for u in usuarios])


@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401
    if user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado: se requiere rol admin'}), 403

    usuario = app_instance.get_user(id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(_user_to_dict(usuario))


@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401
    if user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado: se requiere rol admin'}), 403

    usuario = app_instance.get_user(id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json()
    try:
        app_instance.update_user(
            id,
            nombre=data.get('nombre'),
            email=data.get('email'),
            rol=data.get('rol')
        )
        return jsonify({'message': 'Usuario actualizado correctamente'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 409


@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401
    if user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado: se requiere rol admin'}), 403

    if not app_instance.get_user(id):
        return jsonify({'error': 'Usuario no encontrado'}), 404

    app_instance.delete_user(id)
    return '', 204
