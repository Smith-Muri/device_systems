"""
Capa de servicios (lógica de negocio) para el recurso "usuarios".

Aquí vive toda la lógica de manipulación de datos (buscar, crear, actualizar,
eliminar, filtrar), separada de las rutas (routes) para que estas últimas
solo se encarguen de recibir la petición HTTP y devolver la respuesta.
"""

from typing import Optional

from app.data.users_db import users_db, get_next_id
from app.schemas.user_schema import UserCreate, UserPatch, UserUpdate, UserRole


def list_users(
    role: Optional[UserRole] = None, is_active: Optional[bool] = None
) -> list[dict]:
    """Retorna la lista de usuarios, aplicando filtros opcionales por rol y estado."""
    resultado = users_db

    if role is not None:
        resultado = [u for u in resultado if u["role"] == role]

    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    return resultado


def find_user_by_id(user_id: int) -> Optional[dict]:
    """Busca un usuario por su ID. Retorna None si no existe."""
    for user in users_db:
        if user["id"] == user_id:
            return user
    return None


def email_exists(email: str, exclude_user_id: Optional[int] = None) -> bool:
    """
    Verifica si ya existe un usuario con ese correo.
    `exclude_user_id` permite excluir de la búsqueda al propio usuario que se
    está actualizando (para no marcar como "duplicado" su propio correo).
    """
    for user in users_db:
        if user["id"] == exclude_user_id:
            continue
        if user["email"].lower() == email.lower():
            return True
    return False


def create_user(user_data: UserCreate) -> dict:
    """Crea un nuevo usuario y lo agrega a la base de datos en memoria."""
    nuevo_usuario = {
        "id": get_next_id(),
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "is_active": user_data.is_active,
    }
    users_db.append(nuevo_usuario)
    return nuevo_usuario


def replace_user(user_id: int, user_data: UserUpdate) -> Optional[dict]:
    """
    Actualiza COMPLETAMENTE un usuario existente (PUT).
    Retorna None si el usuario no existe.
    """
    user = find_user_by_id(user_id)
    if user is None:
        return None

    user["name"] = user_data.name
    user["email"] = user_data.email
    user["role"] = user_data.role
    user["is_active"] = user_data.is_active
    return user


def patch_user(user_id: int, patch_data: UserPatch) -> Optional[dict]:
    """
    Actualiza PARCIALMENTE un usuario existente (PATCH), modificando solo
    los campos enviados por el cliente. Retorna None si el usuario no existe.
    """
    user = find_user_by_id(user_id)
    if user is None:
        return None

    datos_enviados = patch_data.model_dump(exclude_unset=True)

    for campo, valor in datos_enviados.items():
        user[campo] = valor

    return user


def delete_user(user_id: int) -> bool:
    """
    Elimina un usuario por su ID.
    Retorna True si se eliminó, False si el usuario no existía.
    """
    user = find_user_by_id(user_id)
    if user is None:
        return False

    users_db.remove(user)
    return True
