from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.db.session import get_db
from app.models.entities import Bus, Route, Trip, Booking, UserRole

router = APIRouter(prefix='/admin', tags=['admin'])


class AddBusRequest(BaseModel):
    registration_number: str
    capacity: int


class CreateRouteRequest(BaseModel):
    name: str
    source: str
    destination: str


class CreateTripRequest(BaseModel):
    route_id: str
    bus_id: str
    departure_time: datetime
    arrival_time: datetime


@router.post('/add-bus')
def add_bus(payload: AddBusRequest, db: Session = Depends(get_db), _=Depends(require_role(UserRole.admin))):
    bus = Bus(registration_number=payload.registration_number, capacity=payload.capacity)
    db.add(bus)
    db.commit()
    db.refresh(bus)
    return bus


@router.post('/create-route')
def create_route(payload: CreateRouteRequest, db: Session = Depends(get_db), _=Depends(require_role(UserRole.admin))):
    route = Route(name=payload.name, source=payload.source, destination=payload.destination)
    db.add(route)
    db.commit()
    db.refresh(route)
    return route


@router.post('/create-trip')
def create_trip(payload: CreateTripRequest, db: Session = Depends(get_db), _=Depends(require_role(UserRole.admin))):
    trip = Trip(**payload.model_dump())
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.get('/analytics')
def analytics(db: Session = Depends(get_db), _=Depends(require_role(UserRole.admin))):
    total_trips = db.execute(select(func.count(Trip.id))).scalar()
    total_bookings = db.execute(select(func.count(Booking.id))).scalar()
    return {'total_trips': total_trips, 'total_bookings': total_bookings}
