from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import GpsLog
from app.schemas.tracking import GpsUpdateRequest
from app.services.tracking_service import TrackingService
from app.websocket.manager import manager

router = APIRouter(prefix='/tracking', tags=['tracking'])


@router.post('/gps-update')
async def gps_update(payload: GpsUpdateRequest, db: Session = Depends(get_db)):
    entry = GpsLog(**payload.model_dump())
    db.add(entry)
    db.commit()
    await manager.broadcast(str(payload.trip_id), payload.model_dump())
    return {'status': 'ok'}


@router.get('/bus-location/{trip_id}')
def bus_location(trip_id: str, db: Session = Depends(get_db)):
    location = TrackingService.latest_location(db, trip_id)
    if not location:
        raise HTTPException(status_code=404, detail='Location not found')
    return location


@router.websocket('/ws/tracking/{trip_id}')
async def tracking_ws(websocket: WebSocket, trip_id: str):
    await manager.connect(trip_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(trip_id, websocket)
