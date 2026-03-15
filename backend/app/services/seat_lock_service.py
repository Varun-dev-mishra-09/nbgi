from uuid import UUID

from app.core.redis_client import redis_client

LOCK_TTL_SECONDS = 300


class SeatLockService:
    @staticmethod
    def key(trip_id: UUID, seat_number: int) -> str:
        return f'seat_lock:{trip_id}:{seat_number}'

    @classmethod
    def lock_seat(cls, trip_id: UUID, seat_number: int, user_id: UUID) -> bool:
        return bool(
            redis_client.set(cls.key(trip_id, seat_number), str(user_id), nx=True, ex=LOCK_TTL_SECONDS)
        )

    @classmethod
    def release_seat(cls, trip_id: UUID, seat_number: int) -> None:
        redis_client.delete(cls.key(trip_id, seat_number))

    @classmethod
    def is_locked(cls, trip_id: UUID, seat_number: int) -> bool:
        return redis_client.exists(cls.key(trip_id, seat_number)) == 1
