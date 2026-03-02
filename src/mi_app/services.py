from datetime import date
from .models import Alquiler
from .exceptions import (
    ElementoNoEncontradoError,
    VehiculoNoDisponibleError,
    ClienteInactivoError,
    ClienteConAlquilerActivoError,
    AlquilerYaCerradoError,
)
from .storage import (
    VehiculoStorage,
    ClienteStorage,
    AlquilerStorage,
)


class AlquilerService:
    """Contiene la lógica de negocio del sistema."""

    def __init__(
        self,
        alquiler_storage: AlquilerStorage,
        cliente_storage: ClienteStorage,
        vehiculo_storage: VehiculoStorage,
    ) -> None:
        self.alquiler_storage = alquiler_storage
        self.cliente_storage = cliente_storage
        self.vehiculo_storage = vehiculo_storage

    def crear_alquiler(self, cliente_id: int, vehiculo_id: int) -> Alquiler:
        """
        Aplica las reglas de negocio para crear un alquiler.
        """

        cliente = self.cliente_storage.obtener_por_id(cliente_id)
        if cliente is None:
            raise ElementoNoEncontradoError()

        vehiculo = self.vehiculo_storage.obtener_por_id(vehiculo_id)
        if vehiculo is None:
            raise ElementoNoEncontradoError()

        if not cliente.activo:
            raise ClienteInactivoError()

        if not vehiculo.disponible:
            raise VehiculoNoDisponibleError()

        alquiler = Alquiler(
            id=0,
            cliente_id=cliente_id,
            vehiculo_id=vehiculo_id,
            fecha_inicio=date.today(),
            fecha_fin=None,
            activo=True,
        )

        return alquiler

    def devolver_vehiculo(self, alquiler_id: int) -> None:
        alquiler = self.alquiler_storage.obtener_por_id(alquiler_id)

        if alquiler is None:
            raise ElementoNoEncontradoError()

        if not alquiler.activo:
            raise AlquilerYaCerradoError()