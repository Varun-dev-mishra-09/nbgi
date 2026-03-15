from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GpsUpdateRequest(BaseModel):
    trip_id: UUID
    latitude: float
    longitude: float
    speed: float | None = None
    heading: float | None = None


class GpsLocationResponse(BaseModel):
    trip_id: UUID
    latitude: float
    longitude: float
    speed: float | None
    heading: float | None
    recorded_at: datetime
