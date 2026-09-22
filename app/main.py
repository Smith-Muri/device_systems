from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.auth import auth_routes
from app.database.connection import create_tables
from app.middlewares.request_middleware import RequestMiddleware
from app.models import device_model, loan_model, user_model
from app.rate_limit import limiter
from app.routes import device_routes, loan_routes, user_routes


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="device_systems API",
    description="API REST segura para usuarios, dispositivos y prestamos. Incluye autenticacion JWT, control de acceso por roles, CORS, rate limiting y migraciones Alembic.",
    version="5.0.0",
    openapi_tags=[
        {"name": "Users", "description": "Operaciones CRUD sobre usuarios."},
        {"name": "Devices", "description": "Operaciones CRUD sobre dispositivos."},
        {"name": "Loans", "description": "Prestamos, devoluciones y consultas relacionadas."},
        {"name": "Auth", "description": "Registro, autenticacion JWT y perfil del usuario actual."},
        {"name": "Security", "description": "Controles de seguridad y trazabilidad de peticiones."},
        {"name": "Raiz", "description": "Estado del servicio."},
    ],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestMiddleware)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)
app.include_router(loan_routes.history_router)


@app.get("/", tags=["Raiz"], summary="Endpoint de bienvenida", description="Comprueba que la API está disponible.", response_description="Estado de la API.")
def read_root():
    return {
        "app": "device_systems",
        "version": "5.0.0",
        "message": "API REST segura de gestion de usuarios, dispositivos y prestamos. Visita /docs.",
    }
