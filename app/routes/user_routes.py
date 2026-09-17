<<<<<<< Updated upstream
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from app.schemas.user_schema import UserCreate, UserResponse, UserRole
=======
from typing import Literal, Optional

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.schemas.user_schema import (
    UserCreate,
    UserPatch,
    UserResponse,
    UserRole,
    UserUpdate,
)
from app.dependencies.database_dependency import get_db
from app.services import user_service
from app.dependencies.user_dependencies import (
    get_user_or_404,
    validate_email_not_duplicated,
    validate_patch_has_data,
)
from fastapi import Query
>>>>>>> Stashed changes

router = APIRouter(prefix="/users", tags=["Usuarios"])

# "Base de datos" en memoria, con un par de usuarios de ejemplo precargados
# para poder probar los endpoints GET sin necesidad de crear datos primero.
fake_users_db: List[dict] = [
    {
        "id": 1,
        "name": "Smith Murillo",
        "email": "smith.murillo@sena.edu.co",
        "role": UserRole.ADMIN,
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Maria Lopez",
        "email": "maria.lopez@sena.edu.co",
        "role": UserRole.SUPPORT,
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Andres Ruiz",
        "email": "andres.ruiz@sena.edu.co",
        "role": UserRole.USER,
        "is_active": False,
    },
]


<<<<<<< Updated upstream
_next_id = len(fake_users_db) + 1
=======
def _set_custom_headers(response: Response) -> None:
    """Agrega las cabeceras personalizadas a toda respuesta del recurso users."""
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "3.0"
>>>>>>> Stashed changes


@router.get(
    "",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios (con filtros opcionales por rol y estado)",
)
def get_users(
    response: Response,
    db: Session = Depends(get_db),
    role: Optional[UserRole] = Query(
        default=None, description="Filtrar usuarios por rol: admin, support o user."
    ),
    is_active: Optional[bool] = Query(
        default=None, description="Filtrar usuarios por estado activo (true) o inactivo (false)."
    ),
    order_by: Literal["id", "name", "created_at"] = Query(
        default="id", description="Ordenar por id, name o created_at."
    ),
):
<<<<<<< Updated upstream

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    resultado = fake_users_db

    if role is not None:
        resultado = [u for u in resultado if u["role"] == role]

    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    return resultado
=======
    _set_custom_headers(response)
    return user_service.list_users(
        db, role=role, is_active=is_active, order_by=order_by
    )
>>>>>>> Stashed changes


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar un usuario por su ID",
)
def get_user_by_id(
    response: Response,
<<<<<<< Updated upstream
    user_id: int = Path(..., description="ID del usuario a consultar.", ge=1, examples=[1]),
):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    for user in fake_users_db:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se encontró un usuario con id={user_id}",
    )
=======
    db: Session = Depends(get_db),
    user=Depends(get_user_or_404),
):
    _set_custom_headers(response)
    return user
>>>>>>> Stashed changes


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
)
<<<<<<< Updated upstream
def create_user(response: Response, user: UserCreate):
=======
def create_user(response: Response, user: UserCreate, db: Session = Depends(get_db)):
    _set_custom_headers(response)
    validate_email_not_duplicated(db, user.email)
    return user_service.create_user(db, user)
>>>>>>> Stashed changes

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

<<<<<<< Updated upstream
    global _next_id
=======
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
    user=Depends(get_user_or_404),
    db: Session = Depends(get_db),
):
    _set_custom_headers(response)
    validate_email_not_duplicated(db, user_data.email, exclude_user_id=user.id)
    return user_service.replace_user(db, user, user_data)
>>>>>>> Stashed changes

    correo_existente = any(u["email"].lower() == user.email.lower() for u in fake_users_db)
    if correo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario registrado con el correo '{user.email}'",
        )

<<<<<<< Updated upstream
    nuevo_usuario = {
        "id": _next_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }

    fake_users_db.append(nuevo_usuario)
    _next_id += 1

    return nuevo_usuario
=======
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
    user=Depends(get_user_or_404),
    db: Session = Depends(get_db),
):
    _set_custom_headers(response)
    validate_patch_has_data(patch_data)

    if patch_data.email is not None:
        validate_email_not_duplicated(db, patch_data.email, exclude_user_id=user.id)

    return user_service.patch_user(db, user, patch_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un usuario",
    description="Elimina un usuario existente. Retorna 404 si el usuario no existe.",
    response_description="Mensaje confirmando la eliminación.",
)
def delete_user(
    response: Response,
    user=Depends(get_user_or_404),
    db: Session = Depends(get_db),
):
    _set_custom_headers(response)
    user_service.delete_user(db, user)
    return {"detail": f"Usuario con id={user.id} eliminado correctamente."}
>>>>>>> Stashed changes
