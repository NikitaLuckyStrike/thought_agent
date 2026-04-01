from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.api.routes import router as api_router
import os

app = FastAPI(title="Thought Agent API")

# Ensure static directory exists
os.makedirs("app/static", exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return f.read()

app.include_router(api_router)
