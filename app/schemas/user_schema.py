from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRole(str, Enum):

    ADMIN = "admin"
    SUPPORT = "support"
    USER = "user"


class UserBase(BaseModel):
    

    name: str = Field(
        ...,
        min_length=3,
        description="Nombre completo del usuario. Mínimo 3 caracteres.",
        examples=["Smith Murillo"],
    )
    email: EmailStr = Field(
        ...,
        description="Correo electrónico del usuario. Debe tener un formato válido.",
        examples=["Smith.Murillo@sena.edu.co"],
    )
    role: UserRole = Field(
        ...,
        description="Rol del usuario dentro del sistema.",
        examples=["admin"],
    )
    is_active: bool = Field(
        default=True,
        description="Indica si el usuario está activo o inactivo.",
        examples=[True],
    )


class UserCreate(UserBase):
    """Modelo de ENTRADA usado en POST /users."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Smith Murillo",
                "email": "Smith.Murillo@sena.edu.co",
                "role": "admin",
                "is_active": True,
            }
        }
    )


class UserUpdate(UserBase):


    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Smith Murillo",
                "email": "Smith.Murillo@sena.edu.co",
                "role": "support",
                "is_active": True,
            }
        }
    )


class UserPatch(BaseModel):


    name: Optional[str] = Field(
        default=None, min_length=3, description="Nuevo nombre (opcional)."
    )
    email: Optional[EmailStr] = Field(
        default=None, description="Nuevo correo electrónico (opcional)."
    )
    role: Optional[UserRole] = Field(
        default=None, description="Nuevo rol (opcional)."
    )
    is_active: Optional[bool] = Field(
        default=None, description="Nuevo estado activo/inactivo (opcional)."
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"role": "support"}}
    )


class UserResponse(UserBase):
    """
    Modelo de SALIDA (response_model) usado para estandarizar y controlar
    exactamente qué campos se devuelven al cliente en cada respuesta.
    """
    id: int = Field(..., description="Identificador único del usuario.", examples=[1])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Smith Murillo",
                "email": "Smith.Murillo@sena.edu.co",
                "role": "admin",
                "is_active": True,
            }
        }
    )
