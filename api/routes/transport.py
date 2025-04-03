from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import database
import crud
import schemas

router = APIRouter(prefix="/transport", tags=["Emissions CO2 d'un transport"])

@router.get("/list", response_model=schemas.ListeModesTransport)
async def get_list_tranports(db: AsyncSession = Depends(database.get_db)):
    modes_transport = await crud.get_list_transports(db)
    return schemas.ListeModesTransport(modes_transport=modes_transport)

@router.get("/{mode_transport}", response_model=schemas.EmissionCO2Schema)
async def get_emission(mode_transport: str, db: AsyncSession = Depends(database.get_db)):
    emission = await crud.get_emission_co2(db, mode_transport)
    if not emission:
        raise HTTPException(status_code=404, detail="Mode de transport non trouvé")
    return emission
