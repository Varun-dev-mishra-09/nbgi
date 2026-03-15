import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.redis_client import redis_client
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.entities import User, UserRole
from app.schemas.auth import GoogleLoginRequest, OtpSendRequest, OtpVerifyRequest, TokenResponse
from app.tasks.worker import celery_app

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/google-login', response_model=TokenResponse)
def google_login(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    email = f'user-{payload.id_token[:8]}@gmail.com'
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        user = User(name='Google User', email=email, role=UserRole.user)
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token(str(user.id), user.role.value)
    return TokenResponse(access_token=token, role=user.role.value)


@router.post('/otp-send')
def send_otp(payload: OtpSendRequest):
    otp = f'{random.randint(100000, 999999)}'
    redis_client.setex(f'otp:{payload.phone}', 300, otp)
    celery_app.send_task('app.tasks.tasks.send_otp_task', args=[payload.phone, otp])
    return {'message': 'OTP sent'}


@router.post('/otp-verify', response_model=TokenResponse)
def verify_otp(payload: OtpVerifyRequest, db: Session = Depends(get_db)):
    stored = redis_client.get(f'otp:{payload.phone}')
    if stored != payload.otp:
        raise HTTPException(status_code=400, detail='Invalid OTP')

    user = db.execute(select(User).where(User.phone == payload.phone)).scalar_one_or_none()
    if not user:
        user = User(name='Mobile User', phone=payload.phone, role=UserRole.user)
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(str(user.id), user.role.value)
    return TokenResponse(access_token=token, role=user.role.value)
