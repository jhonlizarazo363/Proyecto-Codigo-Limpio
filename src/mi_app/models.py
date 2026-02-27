from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass

class Vehiculo:
    """
    representa un vehículo disponible para alquiler.
    """
    id: int
    marca: str
    modelo: str
    año: int
    color: str
    placa: str
    disponible: bool
    precio_por_dia: float


@dataclass

class Cliente:
    """
    representa un cliente registrado en el sistema.
    """
    id: int
    nombre: str
    telefono: str
    email: str
    direccion : str 
    activo: bool

@dataclass

class Alquiler:
    """
    representa el alquiler de un vehículo por un cliente.
    """
    id: int
    cliente_id: int
    vehiculo_id: int
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    activo: bool


