from typing import Literal, Optional

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.user_dependencies import (
    get_user_or_404,
    validate_email_not_duplicated,
    validate_patch_has_data,
)
from app.schemas.user_schema import (
    UserCreate,
    UserPatch,
    UserResponse,
    UserRole,
    UserUpdate,
)
from app.services import user_service


router = APIRouter(prefix="/users", tags=["Users"])


def _set_custom_headers(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "4.0"


@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK, summary="Listar usuarios", description="Lista usuarios con filtros y ordenamiento opcionales.", response_description="Listado de usuarios.")
def get_users(response: Response, db: Session = Depends(get_db), role: Optional[UserRole] = Query(default=None), is_active: Optional[bool] = Query(default=None), order_by: Literal["id", "name", "created_at"] = Query(default="id")):
    _set_custom_headers(response)
    return user_service.list_users(db, role=role, is_active=is_active, order_by=order_by)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Consultar un usuario", description="Busca un usuario por su identificador.", response_description="Usuario encontrado.")
def get_user_by_id(response: Response, user=Depends(get_user_or_404)):
    _set_custom_headers(response)
    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un usuario", description="Crea un usuario con correo único.", response_description="Usuario creado.")
def create_user(response: Response, user: UserCreate, db: Session = Depends(get_db)):
    _set_custom_headers(response)
    validate_email_not_duplicated(db, user.email)
    return user_service.create_user(db, user)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Actualizar completamente un usuario", description="Reemplaza todos los campos de un usuario existente.", response_description="Usuario actualizado.")
def update_user(response: Response, user_data: UserUpdate, user=Depends(get_user_or_404), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    validate_email_not_duplicated(db, user_data.email, exclude_user_id=user.id)
    return user_service.replace_user(db, user, user_data)


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Actualizar parcialmente un usuario", description="Modifica solo los campos enviados.", response_description="Usuario actualizado.")
def patch_user(response: Response, patch_data: UserPatch, user=Depends(get_user_or_404), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    validate_patch_has_data(patch_data)
    if patch_data.email is not None:
        validate_email_not_duplicated(db, patch_data.email, exclude_user_id=user.id)
    return user_service.patch_user(db, user, patch_data)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, summary="Eliminar un usuario", description="Elimina un usuario existente.", response_description="Confirmación de eliminación.")
def delete_user(response: Response, user=Depends(get_user_or_404), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    user_service.delete_user(db, user)
    return {"detail": f"Usuario con id={user.id} eliminado correctamente."}
