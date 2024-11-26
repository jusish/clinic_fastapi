from sqlalchemy import Column, Integer, String, Date, ForeignKey
from ..database import Base
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    dob = Column(Date)
    contact_info = Column(String)
    date_attended = Column(Date, default=datetime.utcnow)