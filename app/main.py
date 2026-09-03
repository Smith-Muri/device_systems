from fastapi import FastAPI

from app.routes import user_routes

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema **device_systems**.\n\n"
        "Desarrollada como evidencia **GA1-220501096-01-AA1-EV08** "
        "(FastAPI Intermedio: CRUD completo, manejo de errores, "
        "Swagger/OpenAPI y Dependency Injection).\n\n"
        "Permite crear, consultar, filtrar, actualizar (total y parcialmente) "
        "y eliminar usuarios, con validaciones de datos y manejo de errores "
        "estructurado."
    ),
    version="2.0.0",
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
)


app.include_router(user_routes.router)


@app.get("/", tags=["Raíz"], summary="Endpoint de bienvenida")
def read_root():
    """Endpoint raíz, útil para verificar que la API está corriendo."""
    return {
        "app": "device_systems",
        "version": "2.0.0",
        "message": "API REST de gestión de usuarios. Visita /docs para la documentación interactiva.",
    }
