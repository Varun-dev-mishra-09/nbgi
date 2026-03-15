from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.entities import Booking, BookingStatus, Payment, PaymentStatus, Ticket, User
from app.schemas.booking import PaymentOrderRequest
from app.services.payment_service import PaymentService
from app.services.seat_lock_service import SeatLockService
from app.tasks.worker import celery_app

router = APIRouter(prefix='/payments', tags=['payments'])


@router.post('/create-order')
def create_order(payload: PaymentOrderRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    booking = Booking(user_id=user.id, trip_id=payload.trip_id, seat_number=payload.seat_number)
    db.add(booking)
    db.flush()
    order = PaymentService.create_provider_order(payload.provider, 5000)
    payment = Payment(
        booking_id=booking.id,
        provider=payload.provider,
        provider_order_id=order['order_id'],
        amount_paise=order['amount_paise'],
        status=PaymentStatus.created,
    )
    db.add(payment)
    db.commit()
    return {'booking_id': booking.id, 'order': order}


@router.post('/verify')
def verify_payment(booking_id: str, payment_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    booking = db.get(Booking, booking_id)
    if not booking or booking.user_id != user.id:
        raise HTTPException(status_code=404, detail='Booking not found')

    payment = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    payment.provider_payment_id = payment_id
    payment.status = PaymentStatus.paid
    booking.status = BookingStatus.confirmed
    SeatLockService.release_seat(booking.trip_id, booking.seat_number)

    celery_app.send_task('app.tasks.tasks.generate_ticket_task', args=[str(booking.id)])
    db.commit()
    return {'status': 'paid'}


@router.post('/webhook')
def payment_webhook(payload: dict, x_signature: str | None = Header(default=None, alias='X-Signature')):
    provider = payload.get('provider', '')
    if not PaymentService.verify_signature(provider, payload, x_signature):
        raise HTTPException(status_code=400, detail='Invalid signature')
    return {'message': 'Webhook received'}
