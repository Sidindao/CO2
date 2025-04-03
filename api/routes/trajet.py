from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from routes import distance
import database
import schemas
import tools

router = APIRouter(prefix="/distance", tags=["Emissions CO2 pour un trajet"])

@router.get("/calculate", response_model=schemas.CalculEmissionOutput)
async def calculate_emission(mode_transport: str = Query(...),
                            adresse_depart: str = Query(...),
                            adresse_arivee: str = Query(...),
                            db: AsyncSession = Depends(database.get_db)):
    """Renvoie l'emission de co2 d'un mode de transport pour un trajet donné."""
    lat1, lon1 = tools.get_lat_long(adresse_depart)
    lat2, lon2 = tools.get_lat_long(adresse_arivee)

    if mode_transport.split(' ')[0] == "car":
        distance_km = tools.fetch_distance_osrm(mode_transport, lat1, lon1, lat2, lon2)
    else:
        distance_km = tools.haversine(lat1, lon1, lat2, lon2)

    return distance.calculate_emission(mode_transport, distance_km, db)
