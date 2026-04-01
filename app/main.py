from fastapi import FastAPI
from app.api.routes import router as api_router
from app.db.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Thought Agent API")

app.include_router(api_router)
