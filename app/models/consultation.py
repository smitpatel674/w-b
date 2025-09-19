from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ConsultationSchedule(Base):
    __tablename__ = "consultation_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    preferred_date = Column(String(10), nullable=False)  # YYYY-MM-DD format
    preferred_time = Column(String(5), nullable=False)   # HH:MM format
    message = Column(Text, nullable=True)
    status = Column(String(20), default="scheduled")     # scheduled, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<ConsultationSchedule(id={self.id}, name='{self.name}', date='{self.preferred_date}', time='{self.preferred_time}')>"