from fastapi import FastAPI
from .amazon import amazon_routers
from .jumia import jumia_routers
from .database import SessionLocal, engine
from .amazon import amazon_models
from .jumia import jumia_models

amazon_models.Base.metadata.create_all(bind=engine)
jumia_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"Message": "Welcome"}

@app.get("/test")
def api_status():
    return {"Status": "Up an running!!!!!!!"}

app.include_router(amazon_routers.router)
app.include_router(jumia_routers.router)