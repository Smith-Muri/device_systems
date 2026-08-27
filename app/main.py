
from fastapi import FastAPI

from app.routes import user_routes

app = FastAPI(
    title="device_systems",
    description=(
        "API REST para la gestión de usuarios del sistema device_systems. "
        "Permite crear, listar, actualizar y eliminar usuarios, así como filtrar "
    ),
    version="1.0.0",
)


app.include_router(user_routes.router)


@app.get("/", tags=["Raíz"], summary="Endpoint de bienvenida")
def read_root():

    return {
        "app": "device_systems",
        "version": "1.0.0",
        "message": "API REST de gestión de usuarios. Visita /docs para la documentación interactiva.",
    }
