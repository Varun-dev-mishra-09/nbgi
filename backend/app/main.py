from fastapi import FastAPI

from app.api.routes.payments import router as payments_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(payments_router, prefix="/api")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
