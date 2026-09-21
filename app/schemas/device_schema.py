from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=3)
    serial_number: str
    device_type: str
    brand: str | None = None
    is_available: bool = True


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class DevicePatch(BaseModel):
    name: str | None = Field(default=None, min_length=3)
    serial_number: str | None = None
    device_type: str | None = None
    brand: str | None = None
    is_available: bool | None = None


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
