from fastapi import FastAPI

from backend.app.api.recommendations import router as recommendations_router

app = FastAPI(title="AI Personal Assistant API", version="0.1.0")
app.include_router(recommendations_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "AI Personal Assistant API is running"}
