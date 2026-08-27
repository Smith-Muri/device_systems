from typing import List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from app.schemas.user_schema import UserCreate, UserResponse, UserRole

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


_next_id = len(fake_users_db) + 1


@router.get(
    "",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios (con filtros opcionales por rol y estado)",
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

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    resultado = fake_users_db

    if role is not None:
        resultado = [u for u in resultado if u["role"] == role]

    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    return resultado


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar un usuario por su ID",
)
def get_user_by_id(
    response: Response,
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


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
)
def create_user(response: Response, user: UserCreate):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    global _next_id

    correo_existente = any(u["email"].lower() == user.email.lower() for u in fake_users_db)
    if correo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario registrado con el correo '{user.email}'",
        )

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
