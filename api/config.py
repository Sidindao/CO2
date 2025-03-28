import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://sarra:SarraProjet@localhost:5432/transport_co2")