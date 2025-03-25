from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import models

async def get_emission_co2(db: AsyncSession, mode_transport: str):
    query = select(models.EmissionCO2).where(models.EmissionCO2.mode_transport == mode_transport)
    result = await db.execute(query)
    return result.scalar_one_or_none()