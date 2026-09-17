from datetime import datetime
from enum import Enum
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
        examples=["smith.murillo@sena.edu.co"],
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
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Smith Murillo",
                "email": "smith.murillo@sena.edu.co",
                "role": "admin",
                "is_active": True,
            }
        }
    )


class UserResponse(UserBase):
    id: int = Field(..., description="Identificador único del usuario.", examples=[1])
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Smith Murillo",
                "email": "smith.murillo@sena.edu.co",
                "role": "admin",
                "is_active": True,
                "created_at": "2026-09-16T12:00:00",
            }
        }
    )
