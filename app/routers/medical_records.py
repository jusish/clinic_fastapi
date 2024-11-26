from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse, MedicalRecordBulkCreate
from ..models.medical_record import MedicalRecord
from ..utils.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=MedicalRecordResponse)
async def create_record(
    record: MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_record = MedicalRecord(
        patient_id=record.patient_id,
        doctor_id=record.doctor_id,
        diagnosis=record.diagnosis,
        treatment=record.treatment,
        status=record.status,
        date=datetime.utcnow()
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/", response_model=List[MedicalRecordResponse])
async def read_records(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    records = db.query(MedicalRecord).order_by(MedicalRecord.date.desc()).offset(skip).limit(limit).all()
    for record in records:
        if record.date is None:
            record.date = datetime.utcnow()
    return records

@router.get("/{record_id}", response_model=MedicalRecordResponse)
async def read_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record

@router.put("/{record_id}", response_model=MedicalRecordResponse)
async def update_record(
    record_id: int,
    record: MedicalRecordUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Medical record not found")
    
    for key, value in record.dict().items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

@router.delete("/{record_id}")
async def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Medical record not found")
    
    db.delete(db_record)
    db.commit()
    return {"message": "Medical record deleted successfully"}

@router.post("/bulk", response_model=List[MedicalRecordResponse])
async def create_records(
    records_data: MedicalRecordBulkCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_records = []
    for record in records_data.records:
        db_record = MedicalRecord(**record.dict())
        db.add(db_record)
        db_records.append(db_record)
    db.commit()
    for record in db_records:
        db.refresh(record)
    return db_records