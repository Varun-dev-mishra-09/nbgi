from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    docs_url='/docs',
    openapi_url='/openapi.json',
    redoc_url='/redoc',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.middleware('http')
async def rate_limit_stub(request: Request, call_next):
    # Replace with Redis based sliding-window limiter for production hardening
    return await call_next(request)


app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get('/healthz')
def health_check():
    return {'status': 'ok'}
