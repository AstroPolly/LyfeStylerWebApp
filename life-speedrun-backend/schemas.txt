# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    title: str
    startTime: str
    endTime: str
    date: str  # "YYYY-MM-DD"
    isRange: bool
    isRecurring: bool
    recurrenceDays: int
    reminder: bool
    reminderMinutes: int
    color: str
    description: Optional[str] = None
    tags: List[int] = []

class EventOut(EventCreate):
    id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password: str

class VerifyCode(BaseModel):
    email: str
    code: str

class Token(BaseModel):
    access_token: str
    token_type: str