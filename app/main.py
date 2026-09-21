from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.connection import create_tables
from app.models import device_model, loan_model, user_model
from app.routes import device_routes, loan_routes, user_routes


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="device_systems API",
    description="API REST para usuarios, dispositivos y prestamos. Usa SQLAlchemy, SQLite y migraciones Alembic.",
    version="4.0.0",
    openapi_tags=[
        {"name": "Users", "description": "Operaciones CRUD sobre usuarios."},
        {"name": "Devices", "description": "Operaciones CRUD sobre dispositivos."},
        {"name": "Loans", "description": "Prestamos, devoluciones y consultas relacionadas."},
        {"name": "Raiz", "description": "Estado del servicio."},
    ],
)

app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)
app.include_router(loan_routes.history_router)


@app.get("/", tags=["Raiz"], summary="Endpoint de bienvenida", description="Comprueba que la API está disponible.", response_description="Estado de la API.")
def read_root():
    return {
        "app": "device_systems",
        "version": "4.0.0",
        "message": "API REST de gestion de usuarios, dispositivos y prestamos. Visita /docs.",
    }
