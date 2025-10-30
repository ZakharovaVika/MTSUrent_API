from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

# User schemas
class UserBase(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None


class UserCreate(UserBase):
    @validator('phone_number')
    def validate_phone(cls, v):
        if not v.startswith('+'):
            raise ValueError('Phone number must start with +')
        return v

class UserUpdate(BaseModel):
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    rating: Optional[float] = None

class User(UserBase):
    user_id: UUID
    registration_date: datetime
    rating: float

    class Config:
        from_attributes = True

# Scooter schemas
class ScooterBase(BaseModel):
    model: str
    manufacture_date: date
    current_battery: int
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    status_code: str
    qr_code: str

    @validator('current_battery')
    def validate_battery(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Battery must be between 0 and 100')
        return v

class ScooterCreate(ScooterBase):
    pass

class ScooterUpdate(BaseModel):
    model: Optional[str] = None
    current_battery: Optional[int] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    status_code: Optional[str] = None

class Scooter(ScooterBase):
    scooter_id: UUID
    created_datetime: datetime

    class Config:
        from_attributes = True

# Scooter Status schemas
class ScooterStatusBase(BaseModel):
    status_code: str
    status_name: str

class ScooterStatusCreate(ScooterStatusBase):
    pass

class ScooterStatus(ScooterStatusBase):
    description: Optional[str] = None

    class Config:
        from_attributes = True

# Payment Status schemas
class PaymentStatusBase(BaseModel):
    status_code: str
    status_name: str

class PaymentStatusCreate(PaymentStatusBase):
    pass

class PaymentStatus(PaymentStatusBase):
    description: Optional[str] = None

    class Config:
        from_attributes = True

# Tariff schemas
class TariffBase(BaseModel):
    tariff_name: str
    unlock_fee: float
    rate_per_minute: float
    rate_per_km: Optional[float] = None
    is_active: bool = True

    @validator('unlock_fee')
    def validate_unlock_fee(cls, v):
        if v < 0:
            raise ValueError('Unlock fee cannot be negative')
        return v

    @validator('rate_per_minute')
    def validate_rate_per_minute(cls, v):
        if v < 0:
            raise ValueError('Rate per minute cannot be negative')
        return v

class TariffCreate(TariffBase):
    pass

class TariffUpdate(BaseModel):
    tariff_name: Optional[str] = None
    unlock_fee: Optional[float] = None
    rate_per_minute: Optional[float] = None
    rate_per_km: Optional[float] = None
    is_active: Optional[bool] = None

class Tariff(TariffBase):
    tariff_id: UUID
    created_datetime: datetime

    class Config:
        from_attributes = True

# Service Staff schemas
class ServiceStaffBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

class ServiceStaffCreate(ServiceStaffBase):
    pass

class ServiceStaffUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

class ServiceStaff(ServiceStaffBase):
    staff_id: UUID
    created_datetime: datetime

    class Config:
        from_attributes = True

# Ride schemas
class RideBase(BaseModel):
    start_latitude: float
    start_longitude: float
    user_id: UUID
    scooter_id: UUID
    tariff_id: UUID

class RideCreate(RideBase):
    pass

class RideUpdate(BaseModel):
    end_latitude: Optional[float] = None
    end_longitude: Optional[float] = None
    distance: Optional[float] = None
    ride_cost: Optional[float] = None

class Ride(RideBase):
    ride_id: UUID
    start_time: datetime
    end_time: Optional[datetime] = None
    end_latitude: Optional[float] = None
    end_longitude: Optional[float] = None
    distance: float
    ride_cost: float
    created_datetime: datetime

    class Config:
        from_attributes = True

# Payment schemas
class PaymentBase(BaseModel):
    amount: float
    payment_method: str
    status_code: str
    ride_id: UUID

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Payment amount must be positive')
        return v

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    status_code: Optional[str] = None

class Payment(PaymentBase):
    payment_id: UUID
    payment_date: datetime
    created_datetime: datetime

    class Config:
        from_attributes = True

# Maintenance schemas
class MaintenanceBase(BaseModel):
    maintenance_type: str
    scheduled_date: date
    description: Optional[str] = None
    scooter_id: UUID
    staff_id: UUID

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(BaseModel):
    maintenance_type: Optional[str] = None
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Maintenance(MaintenanceBase):
    maintenance_id: UUID
    completed_date: Optional[date] = None
    status: str
    created_datetime: datetime

    class Config:
        from_attributes = True

# Response schemas with relationships
class UserWithRides(User):
    rides: List[Ride] = []

class ScooterWithDetails(Scooter):
    rides: List[Ride] = []
    maintenance_records: List[Maintenance] = []
    status: Optional[ScooterStatus] = None

class RideWithDetails(Ride):
    user: Optional[User] = None
    scooter: Optional[Scooter] = None
    tariff: Optional[Tariff] = None
    payment: Optional[Payment] = None

class TariffWithRides(Tariff):
    rides: List[Ride] = []

class PaymentWithDetails(Payment):
    ride: Optional[Ride] = None
    payment_status: Optional[PaymentStatus] = None

class MaintenanceWithDetails(Maintenance):
    scooter: Optional[Scooter] = None
    staff: Optional[ServiceStaff] = None

class ServiceStaffWithMaintenance(ServiceStaff):
    maintenance_records: List[Maintenance] = []