from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class SpecializationEnum(str, Enum):
    cardiology = "cardiology"
    neurology = "neurology"
    pediatrics = "pediatrics"
    orthopedics = "orthopedics"

class RoleEnum(str, Enum):
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    ADMIN = "ADMIN"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    specialization: SpecializationEnum
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None