from fastapi import APIRouter, Depends, HTTPException , Query
from sqlalchemy.ext.asyncio import AsyncSession
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import database
import crud
import schemas

router = APIRouter(prefix="/co2", tags=["Emissions CO2"])

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
    transports = [
    "Car - Electric",
    "Car - Plug-in Hybrid",
    "Car - Mild Hybrid",
    "Car - High-end Mild Hybrid",
    "Bus",
    "Metro",
    "Tramway",
    "RER",
    "TER",
    "Plane"
    ]

    results = []

    for mode in transports:
        result = await crud.calculer_emission_co2(db, mode, distance_km)
        if result:
            results.append(result)

    return results

@router.get("/{mode_transport}", response_model=schemas.EmissionCO2Schema)
async def get_emission(mode_transport: str, db: AsyncSession = Depends(database.get_db)):
    emission = await crud.get_emission_co2(db, mode_transport)
    if not emission:
        raise HTTPException(status_code=404, detail="Mode de transport non trouvé")
    return emission
