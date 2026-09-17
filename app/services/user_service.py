"""Capa de servicios para la persistencia del recurso "usuarios"."""

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserPatch, UserUpdate, UserRole


def list_users(
    db: Session,
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
    order_by: str = "id",
) -> list[User]:
    """Retorna usuarios aplicando filtros y ordenamiento opcionales."""
    query = select(User)

    if role is not None:
        query = query.filter(User.role == role.value)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    query = query.order_by(getattr(User, order_by))
    return list(db.scalars(query).all())


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Busca un usuario por su ID. Retorna None si no existe."""
    return db.get(User, user_id)


def email_exists(
    db: Session, email: str, exclude_user_id: Optional[int] = None
) -> bool:
    """
    Verifica si ya existe un usuario con ese correo.
    `exclude_user_id` permite excluir de la búsqueda al propio usuario que se
    está actualizando (para no marcar como "duplicado" su propio correo).
    """
    query = select(User.id).where(func.lower(User.email) == email.lower())
    if exclude_user_id is not None:
        query = query.where(User.id != exclude_user_id)
    return db.scalar(query) is not None


def create_user(db: Session, user_data: UserCreate) -> User:
    """Crea un nuevo usuario y lo persiste."""
    new_user = User(
        name=user_data.name,
        email=str(user_data.email),
        role=user_data.role.value,
        is_active=user_data.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def replace_user(db: Session, user: User, user_data: UserUpdate) -> User:
    """
    Actualiza COMPLETAMENTE un usuario existente (PUT).
    Retorna None si el usuario no existe.
    """
    user.name = user_data.name
    user.email = str(user_data.email)
    user.role = user_data.role.value
    user.is_active = user_data.is_active
    db.commit()
    db.refresh(user)
    return user


def patch_user(db: Session, user: User, patch_data: UserPatch) -> User:
    """
    Actualiza PARCIALMENTE un usuario existente (PATCH), modificando solo
    los campos enviados por el cliente. Retorna None si el usuario no existe.
    """
    datos_enviados = patch_data.model_dump(exclude_unset=True)

    for campo, valor in datos_enviados.items():
        if campo == "email":
            valor = str(valor)
        elif campo == "role":
            valor = valor.value
        setattr(user, campo, valor)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> bool:
    """
    Elimina un usuario por su ID.
    Retorna True si se eliminó, False si el usuario no existía.
    """
    db.delete(user)
    db.commit()
    return True
