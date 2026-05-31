class Alojamiento:
    def __init__(self, id, titulo, tipo, ciudad, direccion,
                 precio_noche, capacidad, descripcion, servicios, imagen_url):
        self.id = id
        self.titulo = titulo
        self.tipo = tipo
        self.ciudad = ciudad
        self.direccion = direccion
        self.precio_noche = precio_noche
        self.capacidad = capacidad
        self.descripcion = descripcion
        self.servicios = servicios
        self.imagen_url = imagen_url
