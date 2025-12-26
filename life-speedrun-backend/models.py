# models.py
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)                 # "Пить воду"
    description = Column(Text)             # "2 литра в день"
    target_value = Column(Float)           # 2.0
    current_value = Column(Float, default=0.0)
    unit = Column(String)                  # "л", "кг", "шт", "₽"
    frequency = Column(String)             # "daily", "weekly", "monthly", "once"
    start_date = Column(String)            # "2025-06-01"
    deadline = Column(String)              # "2025-12-31"
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BioMetric(Base):
    __tablename__ = "biometrics"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)          # "menstrual", "sleep", "mood", "weight"
    date = Column(String)          # "2025-06-10"
    value = Column(String)         # "start", "peak", "7.2", "good", "bad"
    notes = Column(Text)

# models.py (обновлённый ScheduleEvent)
class ScheduleEvent(Base):
    __tablename__ = "schedule_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    start_time = Column(String)  
    end_time = Column(String)    
    date = Column(String)        
    is_range = Column(Boolean, default=True)
    is_recurring = Column(Boolean, default=False)
    recurrence_days = Column(Integer, default=7)
    reminder = Column(Boolean, default=False)
    reminder_minutes = Column(Integer, default=15)
    color = Column(String, default="#3B82F6")
    description = Column(Text, nullable=True)
    tags = Column(String, nullable=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # === НОВЫЕ ПОЛЯ ДЛЯ СПИДРАНА ===
    actual_start_time = Column(DateTime, nullable=True)     # когда реально начал
    actual_end_time = Column(DateTime, nullable=True)       # когда реально закончил
    completed = Column(Boolean, default=False)              # сделано ли
    notes = Column(Text, nullable=True)                     # комментарий ("кот прыгнул", "вода пролилась")
    