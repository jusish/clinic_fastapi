from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class StatusEnum(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    FOLLOW_UP = "FOLLOW_UP"

class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: int
    diagnosis: str
    treatment: str
    status: StatusEnum

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(MedicalRecordBase):
    pass

class MedicalRecordResponse(MedicalRecordBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True

class MedicalRecordBulkCreate(BaseModel):
    records: List[MedicalRecordCreate]