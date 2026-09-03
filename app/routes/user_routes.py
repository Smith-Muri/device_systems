from typing import Optional

from fastapi import APIRouter, Depends, Response, status

from app.schemas.user_schema import (
    UserCreate,
    UserPatch,
    UserResponse,
    UserRole,
    UserUpdate,
)
from app.services import user_service
from app.dependencies.user_dependencies import (
    get_user_or_404,
    validate_email_not_duplicated,
    validate_patch_has_data,
)
from fastapi import Query

router = APIRouter(prefix="/users", tags=["Users"])


def _set_custom_headers(response: Response) -> None:
    """Agrega las cabeceras personalizadas a toda respuesta del recurso users."""
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"


@router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Lista todos los usuarios registrados. Permite filtrar opcionalmente por rol y por estado activo/inactivo mediante Query Parameters.",
    response_description="Lista de usuarios que cumplen los filtros aplicados.",
)
def get_users(
    response: Response,
    role: Optional[UserRole] = Query(
        default=None, description="Filtrar usuarios por rol: admin, support o user."
    ),
    is_active: Optional[bool] = Query(
        default=None, description="Filtrar usuarios por estado activo (true) o inactivo (false)."
    ),
):
    _set_custom_headers(response)
    return user_service.list_users(role=role, is_active=is_active)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar un usuario por ID",
    description="Retorna un único usuario según el ID enviado como Path Parameter. Si no existe, retorna 404.",
    response_description="Usuario encontrado.",
)
def get_user_by_id(response: Response, user: dict = Depends(get_user_or_404)):
    _set_custom_headers(response)
    return user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
    description="Crea un nuevo usuario. Valida los datos con Pydantic y evita correos duplicados.",
    response_description="Usuario creado, incluyendo su nuevo ID.",
)
def create_user(response: Response, user: UserCreate):
    _set_custom_headers(response)
    validate_email_not_duplicated(user.email)
    return user_service.create_user(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar completamente un usuario",
    description="Reemplaza TODA la información de un usuario existente. Todos los campos son obligatorios. Retorna 404 si el usuario no existe.",
    response_description="Usuario actualizado.",
)
def update_user(
    response: Response,
    user_data: UserUpdate,
    user: dict = Depends(get_user_or_404),
):
    _set_custom_headers(response)
    validate_email_not_duplicated(user_data.email, exclude_user_id=user["id"])
    return user_service.replace_user(user["id"], user_data)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente un usuario",
    description="Modifica solo los campos enviados por el cliente. Retorna 400 si no se envía ningún campo, o 404 si el usuario no existe.",
    response_description="Usuario actualizado con los campos modificados.",
)
def patch_user(
    response: Response,
    patch_data: UserPatch,
    user: dict = Depends(get_user_or_404),
):
    _set_custom_headers(response)
    validate_patch_has_data(patch_data)

    if patch_data.email is not None:
        validate_email_not_duplicated(patch_data.email, exclude_user_id=user["id"])

    return user_service.patch_user(user["id"], patch_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un usuario",
    description="Elimina un usuario existente. Retorna 404 si el usuario no existe.",
    response_description="Mensaje confirmando la eliminación.",
)
def delete_user(response: Response, user: dict = Depends(get_user_or_404)):
    _set_custom_headers(response)
    user_service.delete_user(user["id"])
    return {"detail": f"Usuario con id={user['id']} eliminado correctamente."}
