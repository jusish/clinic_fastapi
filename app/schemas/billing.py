from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class BillingRecordBase(BaseModel):
    patient_id: int
    total_cost: float

class BillingRecordCreate(BillingRecordBase):
    pass

class BillingRecordUpdate(BillingRecordBase):
    pass

class BillingRecordResponse(BillingRecordBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True

class BillingRecordBulkCreate(BaseModel):
    records: List[BillingRecordCreate]