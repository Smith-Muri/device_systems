from fastapi import HTTPException, Path, status

from app.schemas.user_schema import UserPatch
from app.services import user_service


def get_user_or_404(
    user_id: int = Path(..., description="ID del usuario.", ge=1, examples=[1])
) -> dict:

    user = user_service.find_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario no encontrado (id={user_id})",
        )
    return user


def validate_email_not_duplicated(email: str, exclude_user_id: int | None = None) -> None:
  
    if user_service.email_exists(email, exclude_user_id=exclude_user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario registrado con el correo '{email}'",
        )


def validate_patch_has_data(patch_data: UserPatch) -> UserPatch:
    
    datos_enviados = patch_data.model_dump(exclude_unset=True)
    if not datos_enviados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar.",
        )
    return patch_data


def get_api_settings() -> dict:
 
    return {"app_name": "device_systems", "api_version": "2.0.0"}
