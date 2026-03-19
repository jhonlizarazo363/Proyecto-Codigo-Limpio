class RentSystemException(Exception):
    """Clase base para las excepciones del sistema."""

    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(mensaje)


class ElementoNoEncontradoError(RentSystemException):
    """Excepción para indicar que un elemento no fue encontrado."""

    def __init__(self, tipo_elemento: str, elemento_id: int):
        mensaje = f"{tipo_elemento} con ID {elemento_id} no fue encontrado."
        self.tipo_elemento = tipo_elemento
        self.elemento_id = elemento_id
        super().__init__(mensaje)


class VehiculoNoDisponibleError(RentSystemException):
    """Excepción para indicar que un vehículo no está disponible para alquiler."""

    def __init__(self, vehiculo_id: int):
        mensaje = f"El vehículo con ID {vehiculo_id} no está disponible."
        self.vehiculo_id = vehiculo_id
        super().__init__(mensaje)


class ClienteInactivoError(RentSystemException):
    """Excepción para indicar que el cliente no puede alquilar."""

    def __init__(self, cliente_id: int):
        mensaje = f"El cliente con ID {cliente_id} no está activo."
        self.cliente_id = cliente_id
        super().__init__(mensaje)


class ClienteConAlquilerActivoError(RentSystemException):
    """Excepción para indicar que el cliente ya tiene un alquiler activo."""

    def __init__(self, cliente_id: int):
        mensaje = f"El cliente con ID {cliente_id} ya tiene un alquiler activo."
        self.cliente_id = cliente_id
        super().__init__(mensaje)


class AlquilerYaFinalizadoError(RentSystemException):
    """Excepción para indicar que el alquiler ya ha sido finalizado."""

    def __init__(self, alquiler_id: int):
        mensaje = f"El alquiler con ID {alquiler_id} ya fue finalizado."
        self.alquiler_id = alquiler_id
        super().__init__(mensaje)