from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
import models
import schemas

async def get_list_transports(db:AsyncSession):
    query = select(models.EmissionCO2.mode_transport)
    result = await db.execute(query)
    modes_transport = result.scalars().all()
    return [schemas.ModeTransportSchema(mode_transport=mode) for mode in modes_transport]

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
