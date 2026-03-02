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

    
    def crear_alquiler(self, cliente_id: int, vehiculo_id: int) -> Alquiler:
        """
        Crea un alquiler si se cumplen todas las reglas del negocio.

        :raises ElementoNoEncontradoError:
        :raises ClienteInactivoError:
        :raises VehiculoNoDisponibleError:
        :raises ClienteConAlquilerActivoError:
        """

        cliente = self._cliente_storage.obtener_por_id(cliente_id)
        if not cliente:
            raise ElementoNoEncontradoError("Cliente no encontrado.")

        if not cliente.activo:
            raise ClienteInactivoError("El cliente no está activo.")

        vehiculo = self._vehiculo_storage.obtener_por_id(vehiculo_id)
        if not vehiculo:
            raise ElementoNoEncontradoError("Vehículo no encontrado.")

        if not vehiculo.disponible:
            raise VehiculoNoDisponibleError(
                "El vehículo no está disponible."
            )

        alquileres = self._alquiler_storage.obtener_todos()
        for alquiler in alquileres:
            if alquiler.cliente_id == cliente_id and alquiler.activo:
                raise ClienteConAlquilerActivoError(
                    "El cliente ya tiene un alquiler activo."
                )

        nuevo_id = len(alquileres) + 1

        alquiler = Alquiler(
            id=nuevo_id,
            cliente_id=cliente_id,
            vehiculo_id=vehiculo_id,
            fecha_inicio=datetime.now(),
            fecha_fin=None,
            activo=True,
        )
         # Cambiar estado del vehículo
        vehiculo.disponible = False

        # Guardar cambios
        self._alquiler_storage.guardar(alquiler)

        return alquiler


    def devolver_vehiculo(self, alquiler_id: int) -> Alquiler:
        """
        Finaliza un alquiler activo.

        :raises ElementoNoEncontradoError:
        :raises AlquilerYaFinalizadoError:
        """

        alquiler = self._alquiler_storage.obtener_por_id(alquiler_id)
        if not alquiler:
            raise ElementoNoEncontradoError("Alquiler no encontrado.")

        if not alquiler.activo:
            raise AlquilerYaFinalizadoError(
                "El alquiler ya fue finalizado."
            )

        alquiler.fecha_fin = datetime.now()
        alquiler.activo = False

        # Volver disponible el vehículo
        vehiculo = self._vehiculo_storage.obtener_por_id(
            alquiler.vehiculo_id
        )
        if vehiculo:
            vehiculo.disponible = True

        return alquiler

    # ------------------------------------------------------
    # LISTAR ALQUILERES
    # ------------------------------------------------------

    def listar_alquileres(self) -> List[Alquiler]:
        """
        Retorna todos los alquileres registrados.
        """
        return self._alquiler_storage.obtener_todos()
