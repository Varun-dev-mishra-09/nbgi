from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.entities import Route, Trip, Booking, BookingStatus, Ticket, User
from app.schemas.booking import BookSeatRequest, TicketResponse
from app.services.seat_lock_service import SeatLockService

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/routes')
def routes(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.execute(select(Route)).scalars().all()


@router.get('/trips')
def trips(route_id: str | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    stmt = select(Trip)
    if route_id:
        stmt = stmt.where(Trip.route_id == route_id)
    return db.execute(stmt).scalars().all()


@router.post('/book-seat')
def book_seat(payload: BookSeatRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    already = db.execute(
        select(Booking).where(
            Booking.trip_id == payload.trip_id,
            Booking.seat_number == payload.seat_number,
            Booking.status == BookingStatus.confirmed,
        )
    ).scalar_one_or_none()
    if already:
        raise HTTPException(status_code=409, detail='Seat already booked')

    if not SeatLockService.lock_seat(payload.trip_id, payload.seat_number, user.id):
        raise HTTPException(status_code=409, detail='Seat locked by another user')

    booking = Booking(user_id=user.id, trip_id=payload.trip_id, seat_number=payload.seat_number)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return {'booking_id': booking.id, 'status': booking.status.value}


@router.get('/ticket/{booking_id}', response_model=TicketResponse)
def get_ticket(booking_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    ticket = db.execute(select(Ticket).where(Ticket.booking_id == booking_id)).scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')

    booking = db.get(Booking, booking_id)
    return TicketResponse(
        booking_id=booking.id,
        trip_id=booking.trip_id,
        seat_number=booking.seat_number,
        qr_payload=ticket.qr_payload,
    )
