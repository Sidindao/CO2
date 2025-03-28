from sqlalchemy.future import select 
from sqlalchemy.ext.asyncio import AsyncSession
from api import models
from sqlalchemy import func

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
    return {
        "mode_transport": emission.mode_transport,  # on renvoie le vrai nom
        "distance_km": distance_km,
        "total_emission": total_emission
    }

