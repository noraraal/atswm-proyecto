from flask import Blueprint, request, jsonify, make_response
from backend.sessions import create_session, delete_session

auth_bp = Blueprint('auth', __name__)

# La instancia de ReservasApp se inyecta desde app.py
app_instance = None


@auth_bp.route('/auth/registro', methods=['POST'])
def registro():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not nombre or not email or not password:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400
    if len(password) < 8:
        return jsonify({'error': 'La contrasena debe tener al menos 8 caracteres'}), 400

    try:
        app_instance.register_user(nombre, email, password)
        return jsonify({'message': 'Usuario registrado correctamente'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    user = app_instance.validate_credentials(email, password)
    if not user:
        return jsonify({'error': 'Credenciales incorrectas'}), 401

    token = create_session(user.id)
    resp = make_response(jsonify({'message': 'Login exitoso'}))
    resp.set_cookie(
        key='session',
        value=token,
        httponly=True,
        samesite='Lax',
        path='/api'
    )
    return resp


@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    token = request.cookies.get('session')
    if token:
        delete_session(token)
    resp = make_response(jsonify({'message': 'Logout correcto'}))
    resp.delete_cookie('session', path='/api')
    return resp
