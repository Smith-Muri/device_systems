from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.services import device_service


def get_device_or_404(device_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    device = device_service.get_device_by_id(db, device_id)
    if device is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dispositivo no encontrado (id={device_id})")
    return device
