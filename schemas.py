from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class PatientInfoCreate(BaseModel):
    name: str
    date_of_birth: date
    gender: str
    national_id: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    blood_type: Optional[str] = None


class PatientInfoOut(PatientInfoCreate):
    id: int
    first_visit_date: Optional[date] = None
    last_visit_date: Optional[date] = None
    total_visit_count: Optional[int] = None
    last_prescription_id: Optional[int] = None

    class Config:
        from_attributes = True


class AppointmentCreate(BaseModel):
    patient_id: int
    appointment_day: Optional[datetime] = None


class AppointmentRead(BaseModel):
    id: int
    patient_id: int
    created_at: datetime
    appointment_day: datetime

    class Config:
        from_attributes = True  # Updated from orm_mode = True for Pydantic v2
