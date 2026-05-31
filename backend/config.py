# Configuración global de la aplicación
import os

# --- Base de datos ---
# Usa la variable de entorno DATABASE_URL si existe;
# si no, SQLite local para desarrollo.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///reservas.db"
)

# Azure PostgreSQL (cuando se despliegue en la VM):
# DATABASE_URL=postgresql+psycopg2://reservas_user:reservas_passwd@localhost:5432/reservas_db

# --- Flask ---
SECRET_KEY = os.environ.get("SECRET_KEY", "clave-secreta-desarrollo")
