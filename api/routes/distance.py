from fastapi import APIRouter, Depends, HTTPException , Query
from sqlalchemy.ext.asyncio import AsyncSession
import database
import crud
import schemas

router = APIRouter(prefix="/distance", tags=["Emissions CO2 pour une distance"])

@router.get("/calculate", response_model=schemas.CalculEmissionOutput)
async def calculate_emission(
    mode_transport: str = Query(...),
    distance_km: float = Query(...),
    db: AsyncSession = Depends(database.get_db)
):
    result = await crud.calculer_emission_co2(db, mode_transport, distance_km)
    if not result:
        raise HTTPException(status_code=404, detail="Mode de transport non trouvé")
    return result

@router.get("/compare", response_model=list[schemas.CalculEmissionOutput])
async def compare_emissions(
    distance_km: float = Query(...),
    db: AsyncSession = Depends(database.get_db)):

    transports = (await crud.get_list_transports(db)).modes_transports

    results = []

    for mode in transports:
        result = await crud.calculer_emission_co2(db, mode, distance_km)
        if result:
            results.append(result)

    return results
