from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.billing import BillingRecordCreate, BillingRecordUpdate, BillingRecordResponse, BillingRecordBulkCreate
from ..models.billing import BillingRecord
from ..utils.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=BillingRecordResponse)
async def create_billing(
    billing: BillingRecordCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_billing = BillingRecord(**billing.dict())
    db.add(db_billing)
    db.commit()
    db.refresh(db_billing)
    return db_billing

@router.get("/", response_model=List[BillingRecordResponse])
async def read_billings(
    skip: int = 0,
    limit: int = 500000,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    billings = db.query(BillingRecord).offset(skip).limit(limit).all()
    return billings

@router.get("/{billing_id}", response_model=BillingRecordResponse)
async def read_billing(
    billing_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    billing = db.query(BillingRecord).filter(BillingRecord.id == billing_id).first()
    if billing is None:
        raise HTTPException(status_code=404, detail="Billing record not found")
    return billing

@router.put("/{billing_id}", response_model=BillingRecordResponse)
async def update_billing(
    billing_id: int,
    billing: BillingRecordUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_billing = db.query(BillingRecord).filter(BillingRecord.id == billing_id).first()
    if db_billing is None:
        raise HTTPException(status_code=404, detail="Billing record not found")
    
    for key, value in billing.dict().items():
        setattr(db_billing, key, value)
    
    db.commit()
    db.refresh(db_billing)
    return db_billing

@router.delete("/{billing_id}")
async def delete_billing(
    billing_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_billing = db.query(BillingRecord).filter(BillingRecord.id == billing_id).first()
    if db_billing is None:
        raise HTTPException(status_code=404, detail="Billing record not found")
    
    db.delete(db_billing)
    db.commit()
    return {"message": "Billing record deleted successfully"}

@router.post("/bulk", response_model=List[BillingRecordResponse])
async def create_billing_records(
    records_data: BillingRecordBulkCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_records = []
    for record in records_data.records:
        db_record = BillingRecord(**record.dict())
        db.add(db_record)
        db_records.append(db_record)
    db.commit()
    for record in db_records:
        db.refresh(record)
    return db_records