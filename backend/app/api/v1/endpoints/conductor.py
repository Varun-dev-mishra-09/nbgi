from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.db.session import get_db
from app.models.entities import Booking, BookingStatus, Ticket, Trip, UserRole
from app.schemas.booking import BookSeatRequest

router = APIRouter(prefix='/conductor', tags=['conductor'])


@router.get('/trip/{trip_id}')
def trip_details(trip_id: str, db: Session = Depends(get_db), _=Depends(require_role(UserRole.conductor, UserRole.admin))):
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail='Trip not found')
    bookings = db.execute(select(Booking).where(Booking.trip_id == trip_id)).scalars().all()
    return {'trip': trip, 'bookings': bookings}


@router.post('/book-seat')
def walk_in_booking(payload: BookSeatRequest, db: Session = Depends(get_db), conductor=Depends(require_role(UserRole.conductor, UserRole.admin))):
    booking = Booking(user_id=conductor.id, trip_id=payload.trip_id, seat_number=payload.seat_number, status=BookingStatus.confirmed)
    db.add(booking)
    db.commit()
    return {'status': 'confirmed', 'booking_id': booking.id}


@router.post('/verify-ticket')
def verify_ticket(booking_id: str, db: Session = Depends(get_db), _=Depends(require_role(UserRole.conductor, UserRole.admin))):
    ticket = db.execute(select(Ticket).where(Ticket.booking_id == booking_id)).scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail='Invalid ticket')
    return {'valid': True, 'booking_id': booking_id}
