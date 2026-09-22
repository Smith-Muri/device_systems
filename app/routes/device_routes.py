from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import require_admin, require_admin_or_support
from app.dependencies.device_dependencies import get_device_or_404
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceResponse, DeviceUpdate
from app.schemas.loan_schema import LoanResponse
from app.services import device_service, loan_service


router = APIRouter(prefix="/devices", tags=["Devices"])


def _set_custom_headers(response: Response) -> None:
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "4.0"


@router.get("", response_model=list[DeviceResponse], summary="Listar dispositivos", description="Lista dispositivos aplicando filtros opcionales.", response_description="Listado de dispositivos.")
def list_devices(response: Response, db: Session = Depends(get_db), device_type: str | None = Query(default=None), is_available: bool | None = Query(default=None), brand: str | None = Query(default=None), search: str | None = Query(default=None)):
    _set_custom_headers(response)
    return device_service.list_devices(db, device_type, is_available, brand, search)


@router.get("/{device_id}", response_model=DeviceResponse, summary="Consultar un dispositivo", description="Busca un dispositivo por su identificador.", response_description="Dispositivo encontrado.")
def get_device(response: Response, device=Depends(get_device_or_404)):
    _set_custom_headers(response)
    return device


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un dispositivo", description="Crea un dispositivo con número serial único.", response_description="Dispositivo creado.")
def create_device(response: Response, device_data: DeviceCreate, current_user=Depends(require_admin_or_support), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    if device_service.serial_number_exists(db, device_data.serial_number):
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un dispositivo con ese serial_number")
    return device_service.create_device(db, device_data)


@router.put("/{device_id}", response_model=DeviceResponse, summary="Actualizar completamente un dispositivo", description="Reemplaza todos los campos del dispositivo.", response_description="Dispositivo actualizado.")
def update_device(response: Response, device_data: DeviceUpdate, current_user=Depends(require_admin_or_support), device=Depends(get_device_or_404), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    if device_service.serial_number_exists(db, device_data.serial_number, device.id):
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un dispositivo con ese serial_number")
    return device_service.replace_device(db, device, device_data)


@router.patch("/{device_id}", response_model=DeviceResponse, summary="Actualizar parcialmente un dispositivo", description="Modifica solo los campos enviados.", response_description="Dispositivo actualizado.")
def patch_device(response: Response, patch_data: DevicePatch, device=Depends(get_device_or_404), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    if not patch_data.model_fields_set:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debe enviar al menos un campo para actualizar")
    if patch_data.serial_number is not None and device_service.serial_number_exists(db, patch_data.serial_number, device.id):
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un dispositivo con ese serial_number")
    return device_service.patch_device(db, device, patch_data)


@router.delete("/{device_id}", summary="Eliminar un dispositivo", description="Elimina un dispositivo existente.", response_description="Confirmación de eliminación.")
def delete_device(response: Response, current_user=Depends(require_admin), device=Depends(get_device_or_404), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    device_service.delete_device(db, device)
    return {"detail": f"Dispositivo con id={device.id} eliminado correctamente."}


@router.get("/{device_id}/loans", response_model=list[LoanResponse], summary="Consultar préstamos de un dispositivo", description="Devuelve el historial de préstamos del dispositivo.", response_description="Historial de préstamos.")
def device_loans(response: Response, device=Depends(get_device_or_404), db: Session = Depends(get_db)):
    _set_custom_headers(response)
    return loan_service.get_loans_by_device(db, device.id)
