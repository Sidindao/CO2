from sqlalchemy import Column,Integer,Boolean, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EmissionCO2(Base):
    __tablename__ = "emissions_co2"
    mode_transport = Column(String, primary_key=True)
    emission_par_km = Column(Float, nullable=False)
    
class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)