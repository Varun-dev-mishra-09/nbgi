from fastapi import APIRouter

from app.api.v1.endpoints import auth, user, conductor, admin, payments, tracking

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(conductor.router)
api_router.include_router(admin.router)
api_router.include_router(payments.router)
api_router.include_router(tracking.router)
