from fastapi import APIRouter
from storage.supabase import supabase
from schemas.alquiler import AlquilerCreate
from datetime import datetime

router = APIRouter(tags=["Alquileres"])


@router.get("/alquileres")
def listar_alquileres():

    response = supabase.table("alquiler").select("*").execute()

    return response.data


@router.get("/alquileres/{alquiler_id}")
def obtener_alquiler(alquiler_id: int):

    response = (
        supabase
        .table("alquiler")
        .select("*")
        .eq("id", alquiler_id)
        .execute()
    )

    return response.data


@router.post("/alquileres")
def crear_alquiler(alquiler: AlquilerCreate):

    cliente = (
        supabase
        .table("cliente")
        .select("*")
        .eq("id", alquiler.cliente_id)
        .execute()
    )

    if not cliente.data:
        return {
            "error": "El cliente no existe"
        }

    fecha_inicio = datetime.strptime(
        str(alquiler.fecha_inicio),
        "%Y-%m-%d"
    )

    fecha_fin = datetime.strptime(
        str(alquiler.fecha_fin),
        "%Y-%m-%d"
    )

    if fecha_fin < fecha_inicio:
        return {
            "error": "La fecha final no puede ser menor a la fecha inicial"
        }

    vehiculo = (
        supabase
        .table("vehiculo")
        .select("*")
        .eq("id", alquiler.vehiculo_id)
        .execute()
    )

    if not vehiculo.data:
        return {
            "error": "El vehículo no existe"
        }

    if vehiculo.data[0]["disponible"] == False:
        return {
            "error": "El vehículo no está disponible"
        }

    dias = (fecha_fin - fecha_inicio).days

    if dias <= 0:
        dias = 1

    precio_por_dia = vehiculo.data[0]["precio_por_dia"]

    total = dias * precio_por_dia

    data = {
        "cliente_id": alquiler.cliente_id,
        "vehiculo_id": alquiler.vehiculo_id,
        "fecha_inicio": str(alquiler.fecha_inicio),
        "fecha_fin": str(alquiler.fecha_fin),
        "total": total,
        "activo": True
    }

    response = supabase.table("alquiler").insert(data).execute()

    supabase.table("vehiculo").update({
        "disponible": False
    }).eq("id", alquiler.vehiculo_id).execute()

    return {
        "mensaje": "Alquiler creado correctamente",
        "total_calculado": total,
        "data": response.data
    }


@router.put("/alquileres/{alquiler_id}")
def actualizar_alquiler(alquiler_id: int, alquiler: AlquilerCreate):

    alquiler_existente = (
        supabase
        .table("alquiler")
        .select("*")
        .eq("id", alquiler_id)
        .execute()
    )

    if not alquiler_existente.data:
        return {
            "error": "El alquiler no existe"
        }

    cliente = (
        supabase
        .table("cliente")
        .select("*")
        .eq("id", alquiler.cliente_id)
        .execute()
    )

    if not cliente.data:
        return {
            "error": "El cliente no existe"
        }

    vehiculo = (
        supabase
        .table("vehiculo")
        .select("*")
        .eq("id", alquiler.vehiculo_id)
        .execute()
    )

    if not vehiculo.data:
        return {
            "error": "El vehículo no existe"
        }

    fecha_inicio = datetime.strptime(
        str(alquiler.fecha_inicio),
        "%Y-%m-%d"
    )

    fecha_fin = datetime.strptime(
        str(alquiler.fecha_fin),
        "%Y-%m-%d"
    )

    if fecha_fin < fecha_inicio:
        return {
            "error": "La fecha final no puede ser menor a la inicial"
        }

    dias = (fecha_fin - fecha_inicio).days

    if dias == 0:
        dias = 1

    precio_por_dia = vehiculo.data[0]["precio_por_dia"]

    total = dias * precio_por_dia

    data = {
        "cliente_id": alquiler.cliente_id,
        "vehiculo_id": alquiler.vehiculo_id,
        "fecha_inicio": str(alquiler.fecha_inicio),
        "fecha_fin": str(alquiler.fecha_fin),
        "total": total,
        "activo": True
    }

    response = (
        supabase
        .table("alquiler")
        .update(data)
        .eq("id", alquiler_id)
        .execute()
    )

    return {
        "mensaje": "Alquiler actualizado correctamente",
        "total_calculado": total,
        "data": response.data
    }


@router.delete("/alquileres/{alquiler_id}")
def eliminar_alquiler(alquiler_id: int):

    alquiler = (
        supabase
        .table("alquiler")
        .select("*")
        .eq("id", alquiler_id)
        .execute()
    )

    vehiculo_id = alquiler.data[0]["vehiculo_id"]

    supabase.table("vehiculo").update({
        "disponible": True
    }).eq("id", vehiculo_id).execute()

    response = (
        supabase
        .table("alquiler")
        .delete()
        .eq("id", alquiler_id)
        .execute()
    )

    return {
        "mensaje": "Alquiler eliminado correctamente",
        "data": response.data
    }