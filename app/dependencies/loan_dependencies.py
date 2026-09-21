from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.services import loan_service


def get_loan_or_404(loan_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    loan = loan_service.get_loan_by_id(db, loan_id)
    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Préstamo no encontrado (id={loan_id})")
    return loan
