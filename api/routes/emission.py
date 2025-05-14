from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import EmissionCO2
from database import get_db
from auth import get_current_admin

router = APIRouter(prefix="/admin/emissions", tags=["Admin Emissions"])

#Modifier une émission CO2
@router.put("/{mode_transport}")
async def update_emission(
    mode_transport: str,
    new_value: float,
    db: AsyncSession = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    result = await db.execute(select(EmissionCO2).where(EmissionCO2.mode_transport == mode_transport))
    entry = result.scalar_one_or_none()

    if not entry:
        raise HTTPException(status_code=404, detail="Mode of transport not found")

    entry.emission_par_km = new_value
    await db.commit()
    return {"msg": f"{mode_transport} updated to {new_value} kgCO2/km"}

#Supprimer un mode de transport
@router.delete("/{mode_transport}")
async def delete_emission(
    mode_transport: str,
    db: AsyncSession = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    result = await db.execute(select(EmissionCO2).where(EmissionCO2.mode_transport == mode_transport))
    entry = result.scalar_one_or_none()

    if not entry:
        raise HTTPException(status_code=404, detail="Mode of transport not found")

    await db.delete(entry)
    await db.commit()
    return {"msg": f"{mode_transport} deleted"}

#Ajouter un nouveau mode de transport
@router.post("/")
async def add_emission(
    mode_transport: str,
    emission_par_km: float,
    db: AsyncSession = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    result = await db.execute(select(EmissionCO2).where(EmissionCO2.mode_transport == mode_transport))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Mode already exists")

    new_entry = EmissionCO2(mode_transport=mode_transport, emission_par_km=emission_par_km)
    db.add(new_entry)
    await db.commit()
    return {"msg": f"{mode_transport} added with {emission_par_km} kgCO2/km"}

