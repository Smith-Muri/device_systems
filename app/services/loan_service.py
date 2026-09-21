from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate


def list_loans(db: Session, status: str | None = None, user_email: str | None = None, device_type: str | None = None) -> list[Loan]:
    query = select(Loan).join(Loan.user).join(Loan.device)
    if status is not None:
        query = query.where(Loan.status == status)
    if user_email is not None:
        query = query.where(User.email == user_email)
    if device_type is not None:
        query = query.where(Device.device_type == device_type)
    return list(db.scalars(query.order_by(Loan.id)).all())


def get_loan_by_id(db: Session, loan_id: int) -> Loan | None:
    return db.get(Loan, loan_id)


def get_loan_details(db: Session, loan_id: int | None = None) -> list[Loan] | Loan | None:
    query = select(Loan).options(joinedload(Loan.user), joinedload(Loan.device))
    if loan_id is not None:
        return db.scalars(query.where(Loan.id == loan_id)).first()
    return list(db.scalars(query.order_by(Loan.id)).all())


def get_loans_by_user(db: Session, user_id: int) -> list[Loan]:
    return list(db.scalars(select(Loan).where(Loan.user_id == user_id).order_by(Loan.id)).all())


def get_loans_by_device(db: Session, device_id: int) -> list[Loan]:
    return list(db.scalars(select(Loan).where(Loan.device_id == device_id).order_by(Loan.id)).all())


def create_loan(db: Session, loan_data: LoanCreate) -> Loan:
    user = db.get(User, loan_data.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    device = db.get(Device, loan_data.device_id)
    if device is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no encontrado")
    if not device.is_available:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El dispositivo no está disponible")
    loan = Loan(user_id=user.id, device_id=device.id, status="active")
    device.is_available = False
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan: Loan) -> Loan:
    if loan.status == "returned":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El préstamo ya fue devuelto")
    loan.status = "returned"
    loan.return_date = datetime.now()
    loan.device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan
