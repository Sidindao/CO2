from pydantic import BaseModel
from typing import List

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

class ModeTransportSchema(BaseModel):
    mode_transport: str

class ListeModesTransport(BaseModel):
    modes_transport: List[ModeTransportSchema]
