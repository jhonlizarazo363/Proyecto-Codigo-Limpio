from pydantic import BaseModel

class VehiculoCreate(BaseModel):
    marca: str
    modelo: str
    anio: int
    color: str
    placa: str
    precio_por_dia: float

class VehiculoResponse(BaseModel):
    id: int
    marca: str
    modelo: str
    anio: int
    color: str
    placa: str
    disponible: bool
    precio_por_dia: float
