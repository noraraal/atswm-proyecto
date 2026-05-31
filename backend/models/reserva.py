class Reserva:
    def __init__(self, id, cliente_id, alojamiento_id, fecha_entrada,
                 fecha_salida, num_huespedes, precio_total, estado, fecha_reserva):
        self.id = id
        self.cliente_id = cliente_id
        self.alojamiento_id = alojamiento_id
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.num_huespedes = num_huespedes
        self.precio_total = precio_total
        self.estado = estado
        self.fecha_reserva = fecha_reserva
