from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai import ai_router
from ai import populate_chromadb
from .amazon import amazon_routers
from .jumia import jumia_routers
from .database import SessionLocal, engine
from .amazon import amazon_models
from .jumia import jumia_models

amazon_models.Base.metadata.create_all(bind=engine)
jumia_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://localhost:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Message": "Welcome"}

@app.get("/test")
def api_status():
    return {"Status": "Up an running!!!!!!!"}

app.include_router(amazon_routers.router)
app.include_router(jumia_routers.router)
app.include_router(ai_router.router)
app.include_router(populate_chromadb.router)