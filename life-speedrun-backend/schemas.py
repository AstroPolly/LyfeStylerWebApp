# schemas.py — финальная правильная версия (без дублей и с EventUpdate)

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class VerifyCode(BaseModel):
    email: str
    code: str

class Token(BaseModel):
    access_token: str
    token_type: str

class EventCreate(BaseModel):
    title: str
    startTime: str          # "09:00"
    endTime: str            # "10:00"
    date: str               # "2025-06-10"
    isRange: bool
    isRecurring: bool
    recurrenceDays: int
    reminder: bool
    reminderMinutes: int
    color: str
    description: Optional[str] = None
    tags: List[int] = []

class EventUpdate(BaseModel):  # ← ДОБАВЛЕНО
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None
    completed: bool = False
    notes: Optional[str] = None

class EventOut(BaseModel):  # ← не наследуем от EventCreate — явно перечисляем
    id: int
    title: str
    startTime: str
    endTime: str
    date: str
    isRange: bool
    isRecurring: bool
    recurrenceDays: int
    reminder: bool
    reminderMinutes: int
    color: str
    description: Optional[str] = None
    tags: List[int]
    completed: bool
    notes: Optional[str] = None
    duration_seconds: Optional[int] = None  # вычисляется на лету

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }