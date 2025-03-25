from pydantic import BaseModel

class EmissionCO2Schema(BaseModel):
    mode_transport: str
    emission_par_km: float

    class Config:
        orm_mode = True