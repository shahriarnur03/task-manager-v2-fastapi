from sqlalchemy import Column, Integer, String, Boolean

from db.connection import Base

# database table
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=
                True)
    title = Column(String, nullable=False)
    isCompleted = Column(Boolean, default=False)
    
    