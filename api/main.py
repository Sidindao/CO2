from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
import os
from routes import transport, distance, trajet
from routes import emissions


app = FastAPI(title="API CO2 Calculator",
              openapi_url="/openapi.json",
              docs_url="/docs",
              redoc_url="/redoc",
              root_path="/")

origins = ['http://localhost',
           'http://localhost:8080',
           'http://192.168.75.41',
           'http://192.168.75.41/dev/']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transport.router)
app.include_router(distance.router)
app.include_router(trajet.router)
app.include_router(emissions.router)
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
