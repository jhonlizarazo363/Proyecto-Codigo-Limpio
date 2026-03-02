from datetime import datetime
from typing import List

from mi_app.models import Vehiculo, Cliente, Alquiler
from mi_app.storage import VehiculoStorage, ClienteStorage, AlquilerStorage
from mi_app.exceptions import (
    ElementoNoEncontradoError,
    VehiculoNoDisponibleError,
    ClienteInactivoError,
    ClienteConAlquilerActivoError,
    AlquilerYaFinalizadoError,
)


# ==========================================================
# VEHICULO SERVICE
# ==========================================================


class VehiculoService:
    """
    Contiene la lógica de negocio relacionada con los vehículos.
    """

    def __init__(self, vehiculo_storage: VehiculoStorage) -> None:
        self._vehiculo_storage = vehiculo_storage

    def crear_vehiculo(
        self,
        marca: str,
        modelo: str,
        año: int,
        color: str,
        placa: str,
        precio_por_dia: float,
    ) -> Vehiculo:
        """
        Crea un nuevo vehículo disponible.
        """

        vehiculos = self._vehiculo_storage.obtener_todos()
        nuevo_id = len(vehiculos) + 1

        vehiculo = Vehiculo(
            id=nuevo_id,
            marca=marca,
            modelo=modelo,
            año=año,
            color=color,
            placa=placa,
            disponible=True,
            precio_por_dia=precio_por_dia,
        )

        self._vehiculo_storage.guardar(vehiculo)
        return vehiculo

    def listar_vehiculos(self) -> List[Vehiculo]:
        """
        Retorna todos los vehículos registrados.
        """
        return self._vehiculo_storage.obtener_todos()