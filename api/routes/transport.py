from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import database
import crud
import schemas

router = APIRouter(prefix="/co2", tags=["Emissions CO2"])

@router.get("/{mode_transport}", response_model=schemas.EmissionCO2Schema)
async def get_emission(mode_transport: str, db: AsyncSession = Depends(database.get_db)):
    emission = await crud.get_emission_co2(db, mode_transport)
    if not emission:
        raise HTTPException(status_code=404, detail="Mode de transport non trouvé")
    return emission
