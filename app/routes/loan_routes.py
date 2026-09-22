from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support
from app.dependencies.loan_dependencies import get_loan_or_404
from app.dependencies.user_dependencies import get_user_or_404
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanResponse
from app.services import loan_service
from app.rate_limit import limiter


router = APIRouter(prefix="/loans", tags=["Loans"])
history_router = APIRouter(tags=["Loans"])


def _set_custom_headers(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "4.0"


@router.get("", response_model=list[LoanResponse], summary="Listar préstamos", description="Lista préstamos con filtros por estado, correo de usuario y tipo de dispositivo.", response_description="Listado de préstamos.")
def list_loans(response: Response, db: Session = Depends(get_db), status_filter: str | None = Query(default=None, alias="status"), user_email: str | None = None, device_type: str | None = None):
    _set_custom_headers(response)
    return loan_service.list_loans(db, status=status_filter, user_email=user_email, device_type=device_type)


@router.get("/details", response_model=list[LoanDetailResponse], summary="Consultar detalle de préstamos", description="Lista préstamos con usuario y dispositivo anidados.", response_description="Listado detallado de préstamos.")
def list_loan_details(response: Response, current_user=Depends(require_admin_or_support), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    return loan_service.get_loan_details(db)


@router.get("/{loan_id}", response_model=LoanResponse, summary="Consultar un préstamo", description="Busca un préstamo por su identificador.", response_description="Préstamo encontrado.")
def get_loan(response: Response, loan=Depends(get_loan_or_404)):
    _set_custom_headers(response)
    return loan


@router.post("", response_model=LoanResponse, status_code=status.HTTP_201_CREATED, summary="Crear un préstamo", description="Presta un dispositivo disponible a un usuario existente.", response_description="Préstamo creado.")
@limiter.limit("10/minute")
def create_loan(request: Request, response: Response, loan_data: LoanCreate, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    return loan_service.create_loan(db, loan_data)


@router.patch("/{loan_id}/return", response_model=LoanResponse, summary="Devolver un préstamo", description="Marca el préstamo como devuelto y libera el dispositivo.", response_description="Préstamo devuelto.")
def return_loan(response: Response, loan=Depends(get_loan_or_404), current_user=Depends(require_admin_or_support), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    return loan_service.return_loan(db, loan)


@history_router.get("/users/{user_id}/loans", response_model=list[LoanResponse], summary="Consultar préstamos de un usuario", description="Devuelve el historial de préstamos del usuario.", response_description="Historial de préstamos.")
def user_loans(response: Response, user=Depends(get_user_or_404), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    return loan_service.get_loans_by_user(db, user.id)
