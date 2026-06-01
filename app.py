import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.entities.base import engine, Base
# Importar todas las entities para que Base las registre
from backend.entities.usuario_entity import UsuarioEntity      # noqa: F401
from backend.entities.alojamiento_entity import AlojamientoEntity  # noqa: F401
from backend.entities.reserva_entity import ReservaEntity      # noqa: F401

from backend.reservas_app import ReservasApp

from backend.routes.auth_routes import auth_bp
from backend.routes.usuario_routes import usuario_bp
from backend.routes.alojamiento_routes import alojamiento_bp
from backend.routes.reserva_routes import reserva_bp

import backend.routes.auth_routes as auth_mod
import backend.routes.usuario_routes as usuario_mod
import backend.routes.alojamiento_routes as alojamiento_mod
import backend.routes.reserva_routes as reserva_mod


def create_app():
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
    CORS(app, supports_credentials=True)

    # Servir el frontend (HTML/CSS/JS)
    @app.route('/')
    def index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/<path:path>')
    def static_files(path):
        return send_from_directory(frontend_dir, path)

    # Crear tablas en la base de datos
    Base.metadata.create_all(bind=engine)

    # Instancia central de logica de negocio
    reservas_app = ReservasApp()

    # Inyectar la instancia en cada modulo de rutas
    auth_mod.app_instance = reservas_app
    usuario_mod.app_instance = reservas_app
    alojamiento_mod.app_instance = reservas_app
    reserva_mod.app_instance = reservas_app

    # Registrar blueprints bajo /api/v1
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    app.register_blueprint(usuario_bp, url_prefix='/api/v1')
    app.register_blueprint(alojamiento_bp, url_prefix='/api/v1')
    app.register_blueprint(reserva_bp, url_prefix='/api/v1')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
