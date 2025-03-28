import asyncio
from database import get_db, init_db, close_db
from models import EmissionCO2

async def load_data():
    await init_db()
    async for db in get_db():
        data = [
            {"mode_transport": "Car - Electric", "emission_par_km": 0.095},
            {"mode_transport": "Car - Plug-in Hybrid", "emission_par_km": 0.0733},
            {"mode_transport": "Car - Mild Hybrid", "emission_par_km": 0.232},
            {"mode_transport": "Car - High-end Mild Hybrid", "emission_par_km": 0.277},
            {"mode_transport": "Bus", "emission_par_km": 0.166},
            {"mode_transport": "Metro", "emission_par_km": 0.0044},
            {"mode_transport": "Tramway", "emission_par_km": 0.0043},
            {"mode_transport": "RER", "emission_par_km": 0.0098},
            {"mode_transport": "TER", "emission_par_km": 0.0301},
            {"mode_transport": "Plane", "emission_par_km": 0.180},
            {"mode_transport": "TGV", "emission_par_km": 0.00279},
            {"mode_transport": "Bike", "emission_par_km": 0}
        ]
        for d in data:
            db.add(EmissionCO2(**d))
        await db.commit()
    await close_db()

if __name__ == "__main__":
    asyncio.run(load_data())