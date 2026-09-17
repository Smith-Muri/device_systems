<<<<<<< Updated upstream
=======
from contextlib import asynccontextmanager
>>>>>>> Stashed changes

from fastapi import FastAPI

from app.database.connection import create_tables
from app.models import user_model
from app.routes import user_routes


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_tables()
    yield


app = FastAPI(
<<<<<<< Updated upstream
    title="device_systems",
    description=(
        "API REST para la gestión de usuarios del sistema device_systems. "
        "Permite crear, listar, actualizar y eliminar usuarios, así como filtrar "
    ),
    version="1.0.0",
=======
    lifespan=lifespan,
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema **device_systems**.\n\n"
        "Desarrollada como evolución de la evidencia **GA1-220501096-01-AA1-EV08** "
        "(FastAPI Intermedio: CRUD completo, manejo de errores, "
        "Swagger/OpenAPI y Dependency Injection).\n\n"
        "Permite crear, consultar, filtrar, actualizar (total y parcialmente) "
        "y eliminar usuarios, con validaciones de datos y manejo de errores "
        "estructurado. Usa SQLAlchemy y SQLite para persistir los datos."
    ),
    version="3.0.0",
    contact={
        "name": "Smith Murillo - Tecnólogo ADSO",
        "url": "https://github.com/Smith-Muri",
    },
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operaciones CRUD sobre el recurso de usuarios del sistema.",
        },
        {
            "name": "Raíz",
            "description": "Endpoint de verificación del estado del servicio.",
        },
    ],
>>>>>>> Stashed changes
)


app.include_router(user_routes.router)


@app.get("/", tags=["Raíz"], summary="Endpoint de bienvenida")
def read_root():

    return {
        "app": "device_systems",
<<<<<<< Updated upstream
        "version": "1.0.0",
=======
        "version": "3.0.0",
>>>>>>> Stashed changes
        "message": "API REST de gestión de usuarios. Visita /docs para la documentación interactiva.",
    }
