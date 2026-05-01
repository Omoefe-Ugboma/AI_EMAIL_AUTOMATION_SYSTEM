from fastapi import FastAPI
from app.api.routes import router
from app.api.auth_routes import router as auth_router

app = FastAPI(
    title="AI Email Assistant API",
    description="AI-powered email response system",
    version="1.0.0"
)

app.include_router(router)
app.include_router(auth_router)