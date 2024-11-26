from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.inventory import MedicineCreate, MedicineResponse, MedicineBulkCreate
from ..models.inventory import Medicine
from ..utils.auth import get_current_user

router = APIRouter()

@router.post("/medicines/", response_model=MedicineResponse)
async def create_medicine(
    medicine: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_medicine = Medicine(**medicine.dict())
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine

@router.get("/medicines/", response_model=List[MedicineResponse])
async def read_medicines(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    medicines = db.query(Medicine).offset(skip).limit(limit).all()
    return medicines

@router.delete("/medicines/{medicine_id}")
async def delete_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if db_medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    db.delete(db_medicine)
    db.commit()
    return {"message": "Medicine deleted successfully"}

@router.post("/medicines/bulk", response_model=List[MedicineResponse])
async def create_medicines(
    medicines_data: MedicineBulkCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_medicines = []
    for medicine in medicines_data.medicines:
        db_medicine = Medicine(**medicine.dict())
        db.add(db_medicine)
        db_medicines.append(db_medicine)
    db.commit()
    for medicine in db_medicines:
        db.refresh(medicine)
    return db_medicines