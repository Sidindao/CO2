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
    equivalent_en_arbre: int
    

class ListeModesTransport(BaseModel):
    modes_transports: List[str]
