from datetime import datetime
from src.mi_app.models import Vehiculo, Cliente, Alquiler
from src.mi_app.exceptions import (
    ElementoNoEncontradoError,
    ClienteInactivoError,
    VehiculoNoDisponibleError,
    ClienteConAlquilerActivoError,
    AlquilerYaFinalizadoError,
)

# ==========================================================
# VEHICULO SERVICE
# ==========================================================

class VehiculoService:
    def __init__(self, storage):
        self.storage = storage

    def crear_vehiculo(self, marca, modelo, anio, color, placa, precio):
        vehiculos = self.storage.obtener_todos()
        nuevo_id = len(vehiculos) + 1

        vehiculo = Vehiculo(
            nuevo_id,
            marca,
            modelo,
            anio,
            color,
            placa,
            True,
            precio,
        )

        self.storage.guardar(vehiculo)
        return vehiculo
    
    def listar_vehiculos(self):
        return self.storage.obtener_todos()


# ==========================================================
# CLIENTE SERVICE
# ==========================================================


class ClienteService:
    def __init__(self, storage):
        self.storage = storage

    def crear_cliente(self, nombre, telefono, email):
        clientes = self.storage.obtener_todos()
        nuevo_id = len(clientes) + 1

        cliente = Cliente(
            nuevo_id,
            nombre,
            telefono,
            email,
            True,
        )

        self.storage.guardar(cliente)
        return cliente


# ==========================================================
# ALQUILER SERVICE
# ==========================================================



class AlquilerService:
    def __init__(self, alquiler_storage, cliente_storage, vehiculo_storage):
        self.alquiler_storage = alquiler_storage
        self.cliente_storage = cliente_storage
        self.vehiculo_storage = vehiculo_storage


 # ------------------------------------------------------
    # CREAR ALQUILER
    # ------------------------------------------------------


    def crear_alquiler(self, cliente_id, vehiculo_id):
        clientes = self.cliente_storage.obtener_todos()
        vehiculos = self.vehiculo_storage.obtener_todos()
        alquileres = self.alquiler_storage.obtener_todos()

        cliente = next((c for c in clientes if c.id == cliente_id), None)
        if not cliente:
            raise ElementoNoEncontradoError("Cliente no encontrado")

        if not cliente.activo:
            raise ClienteInactivoError("Cliente inactivo")

        vehiculo = next((v for v in vehiculos if v.id == vehiculo_id), None)
        if not vehiculo:
            raise ElementoNoEncontradoError("Vehículo no encontrado")

        if not vehiculo.disponible:
            raise VehiculoNoDisponibleError("Vehículo no disponible")

        alquiler_activo = next(
            (a for a in alquileres if a.cliente_id == cliente_id and a.activo),
            None,
        )

        if alquiler_activo:
            raise ClienteConAlquilerActivoError(
                "Cliente ya tiene alquiler activo"
            )

        nuevo_id = len(alquileres) + 1

        alquiler = Alquiler(
            nuevo_id,
            cliente_id,
            vehiculo_id,
            datetime.now().isoformat(),
            None,
            True,
        )

        vehiculo.disponible = False
        self.vehiculo_storage.actualizar(vehiculo)

        self.alquiler_storage.guardar(alquiler)

        return alquiler


 # ------------------------------------------------------
    # DEVOLVER VEHÍCULO
    # ------------------------------------------------------

    
    def devolver_vehiculo(self, alquiler_id):
        alquileres = self.alquiler_storage.obtener_todos()

        alquiler = next((a for a in alquileres if a.id == alquiler_id), None)

        if not alquiler:
            raise ElementoNoEncontradoError("Alquiler no encontrado")

        if not alquiler.activo:
            raise AlquilerYaFinalizadoError(
                "El alquiler ya fue finalizado"
            )

        alquiler.activo = False
        alquiler.fecha_fin = datetime.now().isoformat()
        self.alquiler_storage.actualizar(alquiler)

        vehiculos = self.vehiculo_storage.obtener_todos()
        vehiculo = next(
            (v for v in vehiculos if v.id == alquiler.vehiculo_id),
            None,
        )

        vehiculo.disponible = True
        self.vehiculo_storage.actualizar(vehiculo)

        return alquiler
