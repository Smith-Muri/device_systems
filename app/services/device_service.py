from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceUpdate


def list_devices(db: Session, device_type: str | None = None, is_available: bool | None = None, brand: str | None = None, search: str | None = None) -> list[Device]:
    query = select(Device)
    if device_type is not None:
        query = query.where(Device.device_type == device_type)
    if is_available is not None:
        query = query.where(Device.is_available == is_available)
    if brand is not None:
        query = query.where(Device.brand == brand)
    if search:
        pattern = f"%{search}%"
        query = query.where(Device.name.ilike(pattern) | Device.serial_number.ilike(pattern))
    return list(db.scalars(query.order_by(Device.id)).all())


def get_device_by_id(db: Session, device_id: int) -> Optional[Device]:
    return db.get(Device, device_id)


def serial_number_exists(db: Session, serial_number: str, exclude_device_id: int | None = None) -> bool:
    query = select(Device.id).where(Device.serial_number == serial_number)
    if exclude_device_id is not None:
        query = query.where(Device.id != exclude_device_id)
    return db.scalar(query) is not None


def create_device(db: Session, device_data: DeviceCreate) -> Device:
    device = Device(**device_data.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def replace_device(db: Session, device: Device, device_data: DeviceUpdate) -> Device:
    for field, value in device_data.model_dump().items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def patch_device(db: Session, device: Device, patch_data: DevicePatch) -> Device:
    for field, value in patch_data.model_dump(exclude_unset=True).items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device: Device) -> bool:
    if db.scalar(select(Loan.id).where(Loan.device_id == device.id)) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un dispositivo con historial de préstamos",
        )
    db.delete(device)
    db.commit()
    return True
