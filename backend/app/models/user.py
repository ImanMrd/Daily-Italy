from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from backend.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    
    # RBAC Role
    role = Column(String(20), default="user", nullable=False)  # "user" or "admin"
    
    # Gamification stats
    xp = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_active_date = Column(String(10), nullable=True)  # YYYY-MM-DD
    hearts = Column(Integer, default=5)
    gems = Column(Integer, default=50)
    
    # Level Access & Progression (e.g. "A1,A2")
    unlocked_levels = Column(String(100), default="A1", nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

