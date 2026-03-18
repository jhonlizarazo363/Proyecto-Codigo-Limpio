import json
from pathlib import Path
from typing import List
from src.mi_app.models import Vehiculo, Cliente, Alquiler

DATABASE_PATH = Path("data/database.json")


class BaseStorage:
    def _leer_db(self):
        # Si el archivo no existe, lo crea con estructura básica
        if not DATABASE_PATH.exists() or DATABASE_PATH.stat().st_size == 0:
            # Estructura base: listas vacías para cada tipo de entidad
            data = {
                "vehiculos": [],
                "clientes": [],
                "alquileres": []
            }
            self._guardar_db(data)
            return data
        
        with open(DATABASE_PATH, "r") as f:
            return json.load(f)

    def _guardar_db(self, data):
        # Asegurarse de que la carpeta "data" exista
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DATABASE_PATH, "w") as f:
            json.dump(data, f, indent=4)


# ==============================
# Vehiculo Storage
# ==============================

class VehiculoStorage(BaseStorage):
    def obtener_todos(self) -> List[Vehiculo]:
        data = self._leer_db()
        return [Vehiculo(**v) for v in data["vehiculos"]]

    def guardar(self, vehiculo: Vehiculo):
        data = self._leer_db()
        data["vehiculos"].append(vehiculo.__dict__)
        self._guardar_db(data)

    def actualizar(self, vehiculo: Vehiculo):
        data = self._leer_db()
        for i, v in enumerate(data["vehiculos"]):
            if v["id"] == vehiculo.id:
                data["vehiculos"][i] = vehiculo.__dict__
                break
        self._guardar_db(data)


# ==============================
# Cliente Storage
# ==============================


class ClienteStorage(BaseStorage):
    def obtener_todos(self) -> List[Cliente]:
        data = self._leer_db()
        return [Cliente(**c) for c in data["clientes"]]

    def guardar(self, cliente: Cliente):
        data = self._leer_db()
        data["clientes"].append(cliente.__dict__)
        self._guardar_db(data)

    def actualizar(self, cliente: Cliente):
        data = self._leer_db()
        for i, c in enumerate(data["clientes"]):
            if c["id"] == cliente.id:
                data["clientes"][i] = cliente.__dict__
                break
        self._guardar_db(data)


# ==============================
# Alquiler Storage
# ==============================


class AlquilerStorage(BaseStorage):
    def obtener_todos(self) -> List[Alquiler]:
        data = self._leer_db()
        return [Alquiler(**a) for a in data["alquileres"]]

    def guardar(self, alquiler: Alquiler):
        data = self._leer_db()
        data["alquileres"].append(alquiler.__dict__)
        self._guardar_db(data)

    def actualizar(self, alquiler: Alquiler):
        data = self._leer_db()
        for i, a in enumerate(data["alquileres"]):
            if a["id"] == alquiler.id:
                data["alquileres"][i] = alquiler.__dict__
                break
        self._guardar_db(data)