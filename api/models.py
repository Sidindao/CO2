from sqlalchemy import Column, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class EmissionCO2(Base):
    __tablename__ = "emissions_co2"
    mode_transport = Column(String, primary_key=True)
    emission_par_km = Column(Float, nullable=False)