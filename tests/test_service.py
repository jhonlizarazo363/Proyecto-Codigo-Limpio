import json
import pytest 
from pathlib import Path
from datetime import datetime


from src.mi_app.services import (
    VehiculoService,
    ClienteService,
    AlquilerService,
)
from src.mi_app.storage import (
    VehiculoStorage,
    ClienteStorage,
    AlquilerStorage,)
from src.mi_app.exceptions import (
    ElementoNoEncontradoError,
    ClienteInactivoError,
    VehiculoNoDisponibleError,
    ClienteConAlquilerActivoError,
    AlquilerYaFinalizadoError,)


@pytest.fixture
def setup_database(tmp_path):
    db_path = tmp_path / "database.json"

    initial_data = {
        "vehiculos": [],
        "clientes": [],
        "alquileres": [],
    }

    with open(db_path, "w") as f:
        json.dump(initial_data, f)

    # parcheamos la ruta global
    # Note: los servicios importan el módulo desde `src.mi_app`, así que aquí debemos
    # patchar el mismo módulo para que use la base de datos temporal.
    from src.mi_app import storage

    storage.DATABASE_PATH = db_path

    return db_path



def test_crear_vehiculo(setup_database):
    storage = VehiculoStorage()
    service = VehiculoService(storage)

    vehiculo = service.crear_vehiculo(
        "Toyota", "Corolla", 2020, "Blanco", "ABC123", 100.0
    )

    assert vehiculo.id == 1
    assert vehiculo.disponible is True



def test_crear_cliente(setup_database):
    storage = ClienteStorage()
    service = ClienteService(storage)

    cliente = service.crear_cliente(
        "Juan", "123456", "juan@test.com"
    )

    assert cliente.id == 1
    assert cliente.activo is True



def test_crear_alquiler_exitoso(setup_database):
    veh_storage = VehiculoStorage()
    cli_storage = ClienteStorage()
    alq_storage = AlquilerStorage()

    veh_service = VehiculoService(veh_storage)
    cli_service = ClienteService(cli_storage)
    alq_service = AlquilerService(
        alq_storage, cli_storage, veh_storage
    )

    cliente = cli_service.crear_cliente(
        "Juan", "123", "juan@test.com"
    )

    vehiculo = veh_service.crear_vehiculo(
        "Toyota", "Corolla", 2020, "Rojo", "XYZ123", 120
    )

    alquiler = alq_service.crear_alquiler(
        cliente.id, vehiculo.id
    )

    assert alquiler.activo is True



def test_cliente_no_existe(setup_database):
    alq_service = AlquilerService(
        AlquilerStorage(),ClienteStorage(),VehiculoStorage()
    )

    with pytest.raises(ElementoNoEncontradoError):
        alq_service.crear_alquiler(999, 999)


def test_cliente_inactivo(setup_database):
    cli_storage = ClienteStorage()
    veh_storage = VehiculoStorage()
    alq_storage = AlquilerStorage()

    cli_service = ClienteService(cli_storage)
    veh_service = VehiculoService(veh_storage)
    alq_service = AlquilerService(
        alq_storage, cli_storage, veh_storage
    )

    cliente = cli_service.crear_cliente(
        "Juan", "123", "juan@test.com"
    )

    # Desactivamos y guardamos correctamente
    cliente.activo = False
    cli_storage.actualizar(cliente)

    vehiculo = veh_service.crear_vehiculo(
        "Mazda", "3", 2022, "Negro", "AAA111", 150
    )

    with pytest.raises(ClienteInactivoError):
        alq_service.crear_alquiler(
            cliente.id, vehiculo.id
        )


def test_vehiculo_no_disponible(setup_database):
    cli_storage = ClienteStorage()
    veh_storage = VehiculoStorage()
    alq_storage = AlquilerStorage()

    cli_service = ClienteService(cli_storage)
    veh_service = VehiculoService(veh_storage)
    alq_service = AlquilerService(
        alq_storage, cli_storage, veh_storage
    )

    cliente = cli_service.crear_cliente(
        "Juan", "123", "juan@test.com"
    )

    vehiculo = veh_service.crear_vehiculo(
        "Toyota", "Corolla", 2020, "Azul", "BBB222", 100
    )

    # lo marcamos no disponible
    vehiculo.disponible = False
    veh_storage.actualizar(vehiculo)

    with pytest.raises(VehiculoNoDisponibleError):
        alq_service.crear_alquiler(
            cliente.id, vehiculo.id
        )


def test_cliente_con_alquiler_activo(setup_database):
    veh_storage = VehiculoStorage()
    cli_storage = ClienteStorage()
    alq_storage = AlquilerStorage()

    veh_service = VehiculoService(veh_storage)
    cli_service = ClienteService(cli_storage)
    alq_service = AlquilerService(
        alq_storage, cli_storage, veh_storage
    )

    cliente = cli_service.crear_cliente(
        "Juan", "123", "juan@test.com"
    )

    v1 = veh_service.crear_vehiculo(
        "Toyota", "Corolla", 2020, "Rojo", "CCC333", 100
    )

    v2 = veh_service.crear_vehiculo(
        "Mazda", "3", 2022, "Negro", "DDD444", 150
    )

    alq_service.crear_alquiler(cliente.id, v1.id)

    with pytest.raises(ClienteConAlquilerActivoError):
        alq_service.crear_alquiler(cliente.id, v2.id)


def test_devolver_alquiler(setup_database):
    veh_storage = VehiculoStorage()
    cli_storage = ClienteStorage()
    alq_storage = AlquilerStorage()

    veh_service = VehiculoService(veh_storage)
    cli_service = ClienteService(cli_storage)
    alq_service = AlquilerService(
        alq_storage, cli_storage, veh_storage
    )

    cliente = cli_service.crear_cliente(
        "Juan", "123", "juan@test.com"
    )

    vehiculo = veh_service.crear_vehiculo(
        "Toyota", "Corolla", 2020, "Rojo", "EEE555", 100
    )

    alquiler = alq_service.crear_alquiler(
        cliente.id, vehiculo.id
    )

    alq_service.devolver_vehiculo(alquiler.id)

    alquiler_actualizado = alq_storage.obtener_todos()[0]

    assert alquiler_actualizado.activo is False


def test_devolver_alquiler_ya_finalizado(setup_database):
    veh_storage = VehiculoStorage()
    cli_storage = ClienteStorage()
    alq_storage = AlquilerStorage()

    veh_service = VehiculoService(veh_storage)
    cli_service = ClienteService(cli_storage)
    alq_service = AlquilerService(
        alq_storage, cli_storage, veh_storage
    )

    cliente = cli_service.crear_cliente(
        "Juan", "123", "juan@test.com"
    )

    vehiculo = veh_service.crear_vehiculo(
        "Toyota", "Corolla", 2020, "Rojo", "FFF666", 100
    )

    alquiler = alq_service.crear_alquiler(
        cliente.id, vehiculo.id
    )

    alq_service.devolver_vehiculo(alquiler.id)

    with pytest.raises(AlquilerYaFinalizadoError):
        alq_service.devolver_vehiculo(alquiler.id)


    


