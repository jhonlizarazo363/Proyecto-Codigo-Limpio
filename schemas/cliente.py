from pydantic import BaseModel

class ClienteCreate(BaseModel):
    nombre: str
    telefono: str
    email: str
