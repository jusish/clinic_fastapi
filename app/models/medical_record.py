from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..database import Base
import enum
from datetime import datetime

class StatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    FOLLOW_UP = "FOLLOW_UP"

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("users.id"))
    diagnosis = Column(String)
    treatment = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.OPEN)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)

    patient = relationship("Patient")
    doctor = relationship("User")