from sqlalchemy import Boolean, Column, Integer, String, Enum
from ..database import Base
import enum

class SpecializationEnum(str, enum.Enum):
    cardiology = "cardiology"
    neurology = "neurology"
    pediatrics = "pediatrics"
    orthopedics = "orthopedics"

class RoleEnum(str, enum.Enum):
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    specialization = Column(Enum(SpecializationEnum))
    role = Column(Enum(RoleEnum))
    is_active = Column(Boolean, default=True)