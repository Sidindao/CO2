from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
from routes import transport


app = FastAPI(title="API CO2 Calculator",
              openapi_url="/api/openapi.json",
              docs_url="/api/docs",
              redoc_url="/api/redoc",
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

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API CO2"}

@app.on_event("startup")
async def startup():
    await database.init_db()
    

@app.on_event("shutdown")
async def shutdown():
    await database.close_db()
    
    
