from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class PatientBase(BaseModel):
    name: str
    dob: date
    contact_info: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    date_attended: date

    class Config:
        from_attributes = True

class PatientBulkCreate(BaseModel):
    patients: List[PatientCreate]