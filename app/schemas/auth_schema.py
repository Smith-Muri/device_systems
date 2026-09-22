from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.user_schema import UserRole


class UserRegister(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if any(character.isspace() for character in password):
            raise ValueError("La contraseña no puede contener espacios en blanco")
        if not any(character.isupper() for character in password):
            raise ValueError("La contraseña debe contener al menos una mayúscula")
        if not any(character.islower() for character in password):
            raise ValueError("La contraseña debe contener al menos una minúscula")
        if not any(character.isdigit() for character in password):
            raise ValueError("La contraseña debe contener al menos un número")
        return password


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserAuthResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
