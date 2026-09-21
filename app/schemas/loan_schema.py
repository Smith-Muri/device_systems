from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LoanCreate(BaseModel):
    user_id: int
    device_id: int


class LoanUpdate(BaseModel):
    status: str | None = None
    return_date: datetime | None = None


class UserBasicInfo(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class DeviceBasicInfo(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = ConfigDict(from_attributes=True)


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: datetime | None
    status: str

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(BaseModel):
    id: int
    status: str
    loan_date: datetime
    return_date: datetime | None
    user: UserBasicInfo
    device: DeviceBasicInfo

    model_config = ConfigDict(from_attributes=True)
