from pydantic import BaseModel
from typing import List

class MedicineBase(BaseModel):
    name: str
    quantity: int

class MedicineCreate(MedicineBase):
    pass

class MedicineResponse(MedicineBase):
    id: int

    class Config:
        from_attributes = True

class MedicineBulkCreate(BaseModel):
    medicines: List[MedicineCreate]