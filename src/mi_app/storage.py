from typing import List, Optional
from .models import Vehiculo, Cliente, Alquiler


class VehiculoStorage:
    """Responsable de persistir vehículos."""

    def guardar(self, vehiculo: Vehiculo) -> None:
        pass

    def obtener_por_id(self, vehiculo_id: int) -> Optional[Vehiculo]:
        pass

    def obtener_todos(self) -> List[Vehiculo]:
        pass


class ClienteStorage:
    """Responsable de persistir clientes."""

    def guardar(self, cliente: Cliente) -> None:
        pass

    def obtener_por_id(self, cliente_id: int) -> Optional[Cliente]:
        pass

    def obtener_todos(self) -> List[Cliente]:
        pass


class AlquilerStorage:
    """Responsable de persistir alquileres."""

    def guardar(self, alquiler: Alquiler) -> None:
        pass

    def obtener_por_id(self, alquiler_id: int) -> Optional[Alquiler]:
        pass

    def obtener_todos(self) -> List[Alquiler]:
        pass