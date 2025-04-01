from pydantic import BaseModel

class EmissionCO2Schema(BaseModel):
    mode_transport: str
    emission_par_km: float

    class Config:
        orm_mode = True

class EmissionCO2Schema(BaseModel):
    mode_transport: str
    emission_par_km: float

    class Config:
        orm_mode = True

class CalculEmissionInput(BaseModel):
    mode_transport: str
    distance_km: float

class CalculEmissionOutput(BaseModel):
    mode_transport: str
    distance_km: float
    total_emission: float
class CalculEmissionOutput(BaseModel):
    mode_transport: str
    distance_km: float
    total_emission: float
