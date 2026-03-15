from uuid import UUID

from pydantic import BaseModel, Field


class BookSeatRequest(BaseModel):
    trip_id: UUID
    seat_number: int = Field(ge=1)


class PaymentOrderRequest(BookSeatRequest):
    provider: str


class TicketResponse(BaseModel):
    booking_id: UUID
    trip_id: UUID
    seat_number: int
    qr_payload: str
