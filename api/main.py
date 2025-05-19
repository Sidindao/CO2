from fastapi import FastAPI
import database
import os
from routes import transport, distance, trajet, admin, emission


app = FastAPI(title="API CO2 Calculator")

app.include_router(transport.router)
app.include_router(distance.router)
app.include_router(trajet.router)
app.include_router(emission.router)
app.include_router(admin.router)

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API CO2"}

@app.on_event("startup")
async def startup():
    if os.getenv("TESTING") != "1":
        await database.init_db()

@app.on_event("shutdown")
async def shutdown():
    await database.close_db()
