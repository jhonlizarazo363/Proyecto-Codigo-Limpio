from fastapi import APIRouter
from storage.supabase import supabase
from schemas.vehiculo_schema import VehiculoCreate

router = APIRouter()


@router.get("/vehiculos")
def listar_vehiculos():
    response = supabase.table("vehiculo").select("*").execute()
    return response.data


@router.get("/vehiculos/disponibles")
def listar_vehiculos_disponibles():

    response = (
        supabase
        .table("vehiculo")
        .select("*")
        .eq("disponible", True)
        .execute()
    )

    return response.data


@router.post("/vehiculos")
def crear_vehiculo(vehiculo: VehiculoCreate):
    data = vehiculo.dict()

    data["disponible"] = True

    response = supabase.table("vehiculo").insert(data).execute()

    return response.data


@router.delete("/vehiculos/{vehiculo_id}")
def eliminar_vehiculo(vehiculo_id: int):
    response = (
        supabase.table("vehiculo")
        .delete()
        .eq("id", vehiculo_id)
        .execute()
    )

    return {
        "mensaje": "Vehículo eliminado correctamente",
        "data": response.data
    }


@router.put("/vehiculos/{vehiculo_id}")
def actualizar_vehiculo(vehiculo_id: int, vehiculo: VehiculoCreate):

    data = vehiculo.dict()

    response = (
        supabase.table("vehiculo")
        .update(data)
        .eq("id", vehiculo_id)
        .execute()
    )

    return {
        "mensaje": "Vehículo actualizado correctamente",
        "data": response.data
    }

@router.get("/vehiculos/{vehiculo_id}")
def obtener_vehiculo(vehiculo_id: int):

    response = (
        supabase
        .table("vehiculo")
        .select("*")
        .eq("id", vehiculo_id)
        .execute()
    )

    if not response.data:
        return {
            "error": "Vehículo no encontrado"
        }

    return response.data

@router.get("/vehiculos/disponibles")
def vehiculos_disponibles():

    response = (
        supabase
        .table("vehiculo")
        .select("*")
        .eq("disponible", True)
        .execute()
    )

    return response.data
