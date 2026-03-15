from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import GpsLog


class TrackingService:
    @staticmethod
    def latest_location(db: Session, trip_id):
        stmt = (
            select(GpsLog)
            .where(GpsLog.trip_id == trip_id)
            .order_by(GpsLog.recorded_at.desc())
            .limit(1)
        )
        return db.execute(stmt).scalar_one_or_none()
