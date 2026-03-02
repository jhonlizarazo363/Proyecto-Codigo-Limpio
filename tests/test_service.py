import json
import pytest
from pathlib import Path
from datetime import datetime

from mi_app.services import (
    VehiculoService,
    ClienteService,
    AlquilerService,
)
from mi_app.storage import (
    VehiculoStorage,
    ClienteStorage,
    AlquilerStorage,
)
from mi_app.exceptions import (
    ElementoNoEncontradoError,
    ClienteInactivoError,
    VehiculoNoDisponibleError,
    ClienteConAlquilerActivoError,
    AlquilerYaFinalizadoError,
)


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
    from mi_app import storage

    storage.DATABASE_PATH = db_path

    return db_path