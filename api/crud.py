from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
import models
import schemas
from tools import co2_to_trees
import tools


async def get_list_transports(db:AsyncSession):
    query = select(models.EmissionCO2.mode_transport)
    result = await db.execute(query)
    modes_transport = result.scalars().all()
    return schemas.ListeModesTransport(modes_transports=modes_transport)

async def get_emission_co2(db: AsyncSession, mode_transport: str):
    query = select(models.EmissionCO2).where(func.lower(models.EmissionCO2.mode_transport) == mode_transport.lower())
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def calculer_emission_co2(db: AsyncSession, mode_transport: str, distance_km: float):
    query = select(models.EmissionCO2).where(
        func.lower(models.EmissionCO2.mode_transport) == mode_transport.strip().lower()
    )
    result = await db.execute(query)
    emission = result.scalar_one_or_none()

    if emission is None:
        return None

    total_emission = emission.emission_par_km * distance_km
    equivalent_en_arbre = int(co2_to_trees(total_emission))
    return {
        "mode_transport": emission.mode_transport,  # on renvoie le vrai nom
        "distance_km": distance_km,
        "total_emission": total_emission,
        "equivalent_en_arbre": equivalent_en_arbre

    }

async def calculer_emission_trajet(mode_transport: str,
                            lat1: float, lon1: float,
                            lat2: float, lon2: float,
                            db: AsyncSession):
    """ if mode_transport.split(' ')[0].lower() == "car":
        distance_km = fetch_distance_osrm("car", lat1, lon1, lat2, lon2)["car"]
    else: """
    distance_km = tools.haversine(lat1, lon1, lat2, lon2)

    if distance_km:
        return await calculer_emission_co2(db, mode_transport, distance_km)
    return None
