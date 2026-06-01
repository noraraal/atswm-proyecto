# Sistema de Reservas para Alojamiento Turístico

Proyecto de la asignatura **Arquitectura y Tecnología de Sistemas Web y Multimedia (ATSWM)** — Grupo 4.

**Autores:** Marc Masana · Nora Raghay

## Descripción

Sistema web para gestionar reservas de alojamientos turísticos en España. Permite a los usuarios buscar hoteles, apartamentos, hostales y casas rurales, registrarse, hacer reservas y cancelarlas. Los administradores gestionan el catálogo de alojamientos y las reservas.

## Arquitectura

```
Cliente (Navegador)
    │
    ▼ HTTPS :443
┌─────────────────────┐
│       NGINX         │  ← Reverse proxy + frontend
│   (Let's Encrypt)   │
└────────┬────────────┘
         │ proxy :5000
┌────────▼────────────┐
│  Flask + Gunicorn   │  ← API REST (/api/v1)
│   (reservas_app)    │
└────────┬────────────┘
         │ :5432
┌────────▼────────────┐
│    PostgreSQL       │  ← Base de datos
│   (reservas_db)     │
└─────────────────────┘
```

## Estructura del proyecto

```
atswm-proyecto/
├── app.py                        # Entrada principal Flask
├── requirements.txt              # Dependencias Python
├── seed.py                       # Datos de prueba
├── frontend/                     # HTML/CSS/JS
│   ├── index.html                # Página principal
│   ├── login.html                # Login
│   ├── registro.html             # Registro
│   ├── alojamientos.html         # Listado con filtros
│   ├── css/style.css
│   └── js/
│       ├── api.js                # Capa de llamadas a la API
│       └── auth.js               # Lógica de autenticación
└── backend/
    ├── config.py                 # Configuración (DB, secret key)
    ├── sessions.py               # Gestión de cookies de sesión
    ├── reservas_app.py           # Lógica de negocio central
    ├── models/                   # Clases de dominio
    ├── entities/                 # SQLAlchemy ORM
    ├── repositories/             # Operaciones CRUD
    └── routes/                   # Endpoints REST
```

## Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/noraraal/atswm-proyecto.git
cd atswm-proyecto

# Crear entorno virtual e instalar dependencias
python -m venv .venv
.venv/Scripts/activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt

# Ejecutar (usa SQLite por defecto)
python app.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`

## Cargar datos de prueba

```bash
python seed.py
```

Crea 5 usuarios, 6 alojamientos y 5 reservas de ejemplo.

## API Endpoints

Base URL: `/api/v1`

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | `/auth/registro` | Registrar usuario | No |
| POST | `/auth/login` | Iniciar sesión | No |
| POST | `/auth/logout` | Cerrar sesión | Sí |
| GET | `/usuarios/me` | Perfil propio | Sí |
| PUT | `/usuarios/me` | Actualizar perfil | Sí |
| GET | `/usuarios` | Listar usuarios | Admin |
| GET/PUT/DELETE | `/usuarios/{id}` | Gestionar usuario | Admin |
| GET | `/alojamientos` | Buscar alojamientos | No |
| GET | `/alojamientos/{id}` | Ver detalle | No |
| GET | `/alojamientos/{id}/disponibilidad` | Comprobar fechas | No |
| POST | `/alojamientos` | Crear alojamiento | Admin |
| PUT | `/alojamientos/{id}` | Actualizar alojamiento | Admin |
| DELETE | `/alojamientos/{id}` | Eliminar alojamiento | Admin |
| POST | `/reservas` | Crear reserva | Cliente |
| GET | `/reservas` | Listar reservas | Sí |
| GET | `/reservas/{id}` | Ver detalle | Sí |
| PATCH | `/reservas/{id}` | Cambiar estado | Sí |
| DELETE | `/reservas/{id}` | Eliminar reserva | Admin |

## Tecnologías

- **Backend:** Python, Flask, SQLAlchemy, Werkzeug
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Servidor:** Azure VM, NGINX, Gunicorn, Let's Encrypt
