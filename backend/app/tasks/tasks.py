import json

import qrcode
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.entities import Booking, Ticket, Notification
from app.tasks.worker import celery_app


@celery_app.task(name='app.tasks.tasks.send_otp_task')
def send_otp_task(phone: str, otp: str):
    return {'phone': phone, 'otp': otp, 'status': 'queued'}


@celery_app.task(name='app.tasks.tasks.generate_ticket_task')
def generate_ticket_task(booking_id: str):
    db = SessionLocal()
    booking = db.execute(select(Booking).where(Booking.id == booking_id)).scalar_one_or_none()
    if not booking:
        return {'error': 'booking not found'}

    payload = {
        'booking_id': str(booking.id),
        'trip_id': str(booking.trip_id),
        'seat_number': booking.seat_number,
    }
    qr_data = json.dumps(payload)
    qrcode.make(qr_data)

    ticket = Ticket(booking_id=booking.id, qr_payload=qr_data)
    notification = Notification(user_id=booking.user_id, title='Ticket Generated', body='Your ticket is now available.')
    db.add(ticket)
    db.add(notification)
    db.commit()
    db.close()
    return payload


@celery_app.task(name='app.tasks.tasks.payment_reconciliation_task')
def payment_reconciliation_task():
    return {'status': 'reconciled'}
