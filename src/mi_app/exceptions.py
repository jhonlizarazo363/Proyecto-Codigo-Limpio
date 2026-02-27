class RentSystemException(Exception):
    """Clase base para las excepciones del sistema."""
    pass

class ElementoNoEncontradoError(RentSystemException):
    """Excepción para indicar que un elemento no fue encontrado."""
    pass 

class VehiculoNoDisponibleError(RentSystemException):
    """Excepción para indicar que un vehículo no está disponible para alquiler."""
    pass

class ClienteInactivoError(RentSystemException):
    """Excepción para indicar que el cliente no puede alquilar."""
    pass

class ClienteConAlquilerActivoError(RentSystemException):
    """Excepción para indicar que el cliente ya tiene un alquiler activo."""
    pass

class AlquilerYaFinalizadoError(RentSystemException):
    """Excepción para indicar que el alquiler ya ha sido finalizadi y se trata de cerrar."""
    pass