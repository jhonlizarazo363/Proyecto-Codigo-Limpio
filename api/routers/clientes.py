from fastapi import APIRouter
from storage.supabase import supabase
from schemas.cliente import ClienteCreate

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("")
def listar_clientes():
    response = supabase.table("cliente").select("*").execute()
    return response.data


@router.post("")
def crear_cliente(cliente: ClienteCreate):

    data = {
        "nombre": cliente.nombre,
        "telefono": cliente.telefono,
        "email": cliente.email,
        "activo": True
    }

    response = supabase.table("cliente").insert(data).execute()

    return {
        "mensaje": "Cliente creado correctamente",
        "data": response.data
    }


@router.put("/{cliente_id}")
def actualizar_cliente(cliente_id: int, cliente: ClienteCreate):

    data = {
        "nombre": cliente.nombre,
        "telefono": cliente.telefono,
        "email": cliente.email,
        "activo": True
    }

    response = (
        supabase
        .table("cliente")
        .update(data)
        .eq("id", cliente_id)
        .execute()
    )

    return {
        "mensaje": "Cliente actualizado correctamente",
        "data": response.data
    }


@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int):

    response = (
        supabase
        .table("cliente")
        .delete()
        .eq("id", cliente_id)
        .execute()
    )

    return {
        "mensaje": "Cliente eliminado correctamente",
        "data": response.data
    }


@router.get("/{cliente_id}")
def obtener_cliente(cliente_id: int):

    response = (
        supabase
        .table("cliente")
        .select("*")
        .eq("id", cliente_id)
        .execute()
    )

    if not response.data:
        return {
            "error": "Cliente no encontrado"
        }

    return response.data
