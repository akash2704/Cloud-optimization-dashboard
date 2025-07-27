from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    resource_type = Column(String)  # 'compute' or 'storage'
    provider = Column(String)  # 'AWS', 'Azure', 'GCP'
    instance_type = Column(String)
    cpu_utilization = Column(Float)  # percentage
    memory_utilization = Column(Float)  # percentage
    storage_gb = Column(Float, nullable=True)
    monthly_cost = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)