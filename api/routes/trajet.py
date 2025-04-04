from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from routes import distance
import database
import schemas
import tools
import crud

router = APIRouter(prefix="/trajet", tags=["Emissions CO2 pour un trajet"])

@router.get("/calculate", response_model=schemas.CalculEmissionOutput)
async def calculate_emission(mode_transport: str = Query(...),
                            adresse_depart: str = Query(...),
                            adresse_arivee: str = Query(...),
                            db: AsyncSession = Depends(database.get_db)):
    """Renvoie l'emission de co2 d'un mode de transport pour un trajet donné."""

    lat1, lon1 = tools.get_lat_long(adresse_depart)
    lat2, lon2 = tools.get_lat_long(adresse_arivee)

    return crud.calculer_emission_trajet(mode_transport, lat1, lon1, lat2, lon2, db)

@router.get("/compare", response_model=list[schemas.CalculEmissionOutput])
async def compare_emissions(adresse_depart: str = Query(...),
                            adresse_arivee: str = Query(...),
                            db: AsyncSession = Depends(database.get_db)):

    transports = (await crud.get_list_transports(db)).modes_transports
    lat1, lon1 = tools.get_lat_long(adresse_depart)
    lat2, lon2 = tools.get_lat_long(adresse_arivee)
    results = []

    for transport in transports:
        result = await crud.calculer_emission_trajet(transport, lat1, lon1, lat2, lon2, db)
        if result:
            results.append(result)

    return results
