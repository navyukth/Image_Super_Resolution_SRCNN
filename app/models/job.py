from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    input_file = Column(String, nullable=False)
    output_file = Column(String, nullable=True)
    status = Column(String, default="processing")
    created_at = Column(DateTime(timezone=True), server_default=func.now())