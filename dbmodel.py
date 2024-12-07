from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class VesselData(Base):
    __tablename__ = 'vessel_data'

    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    group = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Integer, nullable=False)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
