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
    

class ClienteService:
    """
    Contiene la lógica de negocio relacionada con los clientes.
    """

    def __init__(self, cliente_storage: ClienteStorage) -> None:
        self._cliente_storage = cliente_storage

    def crear_cliente(
        self,
        nombre: str,
        telefono: str,
        email: str,
    ) -> Cliente:
        """
        Registra un nuevo cliente activo.
        """

        clientes = self._cliente_storage.obtener_todos()
        nuevo_id = len(clientes) + 1

        cliente = Cliente(
            id=nuevo_id,
            nombre=nombre,
            telefono=telefono,
            email=email,
            activo=True,
        )

        self._cliente_storage.guardar(cliente)
        return cliente

    def listar_clientes(self) -> List[Cliente]:
        """
        Retorna todos los clientes registrados.
        """
        return self._cliente_storage.obtener_todos()
    

class AlquilerService:
    """
    Contiene la lógica de negocio relacionada con los alquileres.
    """

    def __init__(
        self,
        alquiler_storage: AlquilerStorage,
        cliente_storage: ClienteStorage,
        vehiculo_storage: VehiculoStorage,
    ) -> None:
        self._alquiler_storage = alquiler_storage
        self._cliente_storage = cliente_storage
        self._vehiculo_storage = vehiculo_storage
