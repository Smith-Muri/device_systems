from app.schemas.user_schema import UserRole

users_db: list[dict] = [
    {
        "id": 1,
        "name": "Smith Murillo",
        "email": "Smith.Murillo@sena.edu.co",
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


_next_id_counter = {"value": len(users_db) + 1}


def get_next_id() -> int:
    next_id = _next_id_counter["value"]
    _next_id_counter["value"] += 1
    return next_id
