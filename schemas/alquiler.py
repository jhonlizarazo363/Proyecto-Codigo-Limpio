from pydantic import BaseModel
from datetime import date


class AlquilerCreate(BaseModel):
    cliente_id: int
    vehiculo_id: int
    fecha_inicio: date
    fecha_fin: date
