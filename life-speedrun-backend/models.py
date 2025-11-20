# models.py
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

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
    