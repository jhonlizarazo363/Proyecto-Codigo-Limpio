import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from mi_app.models import Vehiculo, Cliente, Alquiler 

DATABASE_PATH = Path("data/database.json")

class DatabaseManager:
    """
    Maneja la lectura y escritura del archivo database.json.
    """

    def _leer_db(self) -> Dict[str, Any]:
        """Lee el archivo JSON y retorna su contenido."""
        if not DATABASE_PATH.exists():
            return {"vehiculos": [], "clientes": [], "alquileres": []}

        with open(DATABASE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    def _guardar_db(self, data: Dict[str, Any]) -> None:
        """Guarda el contenido completo en el archivo JSON."""
        with open(DATABASE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

class VehiculoStorage:
    """Responsable de persistir vehículos."""

    def guardar(self, vehiculo: Vehiculo) -> None:
        data = self._leer_db()
        data["vehiculos"].append(vehiculo.__dict__)
        self._guardar_db(data)

    def obtener_por_id(self, vehiculo_id: int) -> Optional[Vehiculo]:
        data = self._leer_db()
        for item in data["vehiculos"]:
            if item["id"] == vehiculo_id:
                return Vehiculo(**item)
        return None

    def obtener_todos(self) -> List[Vehiculo]:
        data = self._leer_db()
        return [Vehiculo(**item) for item in data["vehiculos"]]

class ClienteStorage:
    """Responsable de persistir clientes."""

    def guardar(self, cliente: Cliente) -> None:
        data = self._leer_db()
        data["clientes"].append(cliente.__dict__)
        self._guardar_db(data)

    def obtener_por_id(self, cliente_id: int) -> Optional[Cliente]:
        data = self._leer_db()
        for item in data["clientes"]:
            if item["id"] == cliente_id:
                return Cliente(**item)
        return None


    def obtener_todos(self) -> List[Cliente]:
        data = self._leer_db()
        return [Cliente(**item) for item in data["clientes"]]



class AlquilerStorage:
    """Responsable de persistir alquileres."""

    def guardar(self, alquiler: Alquiler) -> None:
        data = self._leer_db()

        alquiler_dict = {
            **alquiler.__dict__,
            "fecha_inicio": alquiler.fecha_inicio.isoformat(),
            "fecha_fin": alquiler.fecha_fin.isoformat()
            if alquiler.fecha_fin
            else None,
        }

        data["alquileres"].append(alquiler_dict)
        self._guardar_db(data)

    def obtener_por_id(self, alquiler_id: int) -> Optional[Alquiler]:
        data = self._leer_db()

        for item in data["alquileres"]:
            if item["id"] == alquiler_id:
                return Alquiler(
                    id=item["id"],
                    cliente_id=item["cliente_id"],
                    vehiculo_id=item["vehiculo_id"],
                    fecha_inicio=datetime.fromisoformat(item["fecha_inicio"]),
                    fecha_fin=datetime.fromisoformat(item["fecha_fin"])
                    if item["fecha_fin"]
                    else None,
                    activo=item["activo"],
                )
        return None

    def obtener_todos(self) -> List[Alquiler]:
        data = self._leer_db()

        alquileres: List[Alquiler] = []

        for item in data["alquileres"]:
            alquileres.append(
                Alquiler(
                    id=item["id"],
                    cliente_id=item["cliente_id"],
                    vehiculo_id=item["vehiculo_id"],
                    fecha_inicio=datetime.fromisoformat(item["fecha_inicio"]),
                    fecha_fin=datetime.fromisoformat(item["fecha_fin"])
                    if item["fecha_fin"]
                    else None,
                    activo=item["activo"],
                )
            )

        return alquileres