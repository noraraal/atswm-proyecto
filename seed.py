"""
Carga datos de prueba en la base de datos.
Uso: python seed.py
"""
from app import create_app
from backend.reservas_app import ReservasApp
from datetime import date, timedelta

app = create_app()
ra = ReservasApp()

print("=== Cargando datos de prueba ===\n")

# ---- 1. Usuarios ----
print("1. Creando usuarios...")

usuarios = [
    ("Admin Sistema", "admin@reservas.com", "admin12345"),
    ("Nora Raghay", "nora@gmail.com", "nora12345"),
    ("Marc Masana", "marc@gmail.com", "marc12345"),
    ("Laura Garcia", "laura@gmail.com", "laura1234"),
    ("Carlos Lopez", "carlos@gmail.com", "carlos123"),
]

for nombre, email, password in usuarios:
    try:
        ra.register_user(nombre, email, password)
        print(f"   + {nombre} ({email})")
    except ValueError:
        print(f"   ~ {nombre} ya existe")

# Hacer admin al primer usuario
ra.update_user(1, rol='admin')
print("   * Admin Sistema -> rol admin\n")

# ---- 2. Alojamientos ----
print("2. Creando alojamientos...")

alojamientos = [
    {
        "titulo": "Hotel Mar Azul",
        "tipo": "hotel",
        "ciudad": "Barcelona",
        "direccion": "Passeig de Gracia 42",
        "precio_noche": 120.00,
        "capacidad": 2,
        "descripcion": "Hotel con vistas al mar en el centro de Barcelona",
        "servicios": "wifi,piscina,parking,desayuno",
        "imagen_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945"
    },
    {
        "titulo": "Apartamento Gotico",
        "tipo": "apartamento",
        "ciudad": "Barcelona",
        "direccion": "Carrer dels Banys Nous 15",
        "precio_noche": 85.00,
        "capacidad": 4,
        "descripcion": "Apartamento en el Barrio Gotico con terraza",
        "servicios": "wifi,cocina,lavadora",
        "imagen_url": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688"
    },
    {
        "titulo": "Hostal La Rambla",
        "tipo": "hostal",
        "ciudad": "Barcelona",
        "direccion": "La Rambla 78",
        "precio_noche": 45.00,
        "capacidad": 2,
        "descripcion": "Hostal economico en plena Rambla",
        "servicios": "wifi,desayuno",
        "imagen_url": "https://images.unsplash.com/photo-1555854877-bab0e564b8d5"
    },
    {
        "titulo": "Casa Rural El Pirineo",
        "tipo": "casa",
        "ciudad": "Girona",
        "direccion": "Cami del Bosc 3, Camprodon",
        "precio_noche": 150.00,
        "capacidad": 8,
        "descripcion": "Casa rural con jardin y barbacoa en el Pirineo catalan",
        "servicios": "wifi,parking,jardin,barbacoa,chimenea",
        "imagen_url": "https://images.unsplash.com/photo-1510798831971-661eb04b3739"
    },
    {
        "titulo": "Hotel Playa Dorada",
        "tipo": "hotel",
        "ciudad": "Tarragona",
        "direccion": "Avinguda de la Diputacio 12",
        "precio_noche": 95.00,
        "capacidad": 3,
        "descripcion": "Hotel frente a la playa con piscina exterior",
        "servicios": "wifi,piscina,parking,restaurante",
        "imagen_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4"
    },
    {
        "titulo": "Apartamento Modernista",
        "tipo": "apartamento",
        "ciudad": "Barcelona",
        "direccion": "Carrer de Mallorca 255",
        "precio_noche": 110.00,
        "capacidad": 3,
        "descripcion": "Apartamento de diseno cerca de la Sagrada Familia",
        "servicios": "wifi,cocina,aire acondicionado,balcon",
        "imagen_url": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2"
    },
]

for a in alojamientos:
    try:
        ra.create_alojamiento(**a)
        print(f"   + {a['titulo']} ({a['ciudad']}) - {a['precio_noche']}€/noche")
    except Exception as e:
        print(f"   ! Error creando {a['titulo']}: {e}")

# ---- 3. Reservas ----
print("\n3. Creando reservas...")

hoy = date.today()

reservas = [
    # Nora reserva Hotel Mar Azul (futuro)
    {
        "cliente_id": 2,
        "alojamiento_id": 1,
        "fecha_entrada": hoy + timedelta(days=15),
        "fecha_salida": hoy + timedelta(days=19),
        "num_huespedes": 2
    },
    # Marc reserva Apartamento Gotico (futuro)
    {
        "cliente_id": 3,
        "alojamiento_id": 2,
        "fecha_entrada": hoy + timedelta(days=30),
        "fecha_salida": hoy + timedelta(days=35),
        "num_huespedes": 3
    },
    # Laura reserva Casa Rural (futuro)
    {
        "cliente_id": 4,
        "alojamiento_id": 4,
        "fecha_entrada": hoy + timedelta(days=10),
        "fecha_salida": hoy + timedelta(days=14),
        "num_huespedes": 6
    },
    # Carlos reserva Hotel Playa Dorada (futuro)
    {
        "cliente_id": 5,
        "alojamiento_id": 5,
        "fecha_entrada": hoy + timedelta(days=20),
        "fecha_salida": hoy + timedelta(days=23),
        "num_huespedes": 2
    },
    # Nora reserva Apartamento Modernista (futuro)
    {
        "cliente_id": 2,
        "alojamiento_id": 6,
        "fecha_entrada": hoy + timedelta(days=45),
        "fecha_salida": hoy + timedelta(days=48),
        "num_huespedes": 2
    },
]

for r in reservas:
    try:
        reserva_id, precio = ra.create_reserva(**r)
        nombre = usuarios[r["cliente_id"] - 1][0]
        aloj = alojamientos[r["alojamiento_id"] - 1]["titulo"]
        noches = (r["fecha_salida"] - r["fecha_entrada"]).days
        print(f"   + {nombre} -> {aloj} ({noches} noches, {precio}€)")
    except Exception as e:
        print(f"   ! Error: {e}")

# ---- Resumen ----
print("\n=== Resumen ===")
print(f"   Usuarios:      {len(ra.list_users())}")
print(f"   Alojamientos:  {len(ra.list_alojamientos())}")
print(f"   Reservas:      {len(ra.list_reservas())}")
print("\n=== Credenciales de prueba ===")
print("   Admin:  admin@reservas.com / admin12345")
print("   Nora:   nora@gmail.com / nora12345")
print("   Marc:   marc@gmail.com / marc12345")
print("   Laura:  laura@gmail.com / laura1234")
print("   Carlos: carlos@gmail.com / carlos123")
print("\nDatos cargados correctamente!")
