from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
def api_status():
    return {"Status": "Up an running!!!!!!!"}