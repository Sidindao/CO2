from fastapi import FastAPI
from api import database
from api.routes import transport


app = FastAPI(title="API CO2 Calculator")

app.include_router(transport.router)

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API CO2"}

@app.on_event("startup")
async def startup():
    await database.init_db()
    

@app.on_event("shutdown")
async def shutdown():
    await database.close_db()
    
    
