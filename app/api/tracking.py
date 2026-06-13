from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
import math
from app.core.database import get_db
from app.models.models import LocationPing, Trip, Checkpoint
from app.schemas.schemas import LocationPingCreate, LocationPingOut, LiveLocation

router = APIRouter()

def haversine_m(lat1, lng1, lat2, lng2) -> float:
    """Distance in metres between two GPS coordinates."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi  = math.radians(lat2 - lat1)
    dlam  = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def check_geofences(trip: Trip, lat: float, lng: float, db: Session):
    """Mark checkpoint arrivals when truck enters geofence radius."""
    now = datetime.now(timezone.utc)
    for cp in trip.checkpoints:
        if cp.arrived_at:
            continue
        dist = haversine_m(lat, lng, cp.lat, cp.lng)
        if dist <= cp.radius_m:
            cp.arrived_at = now
            db.add(cp)
    db.commit()

@router.post("/ping", response_model=LocationPingOut)
def post_location(payload: LocationPingCreate, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == payload.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    ping = LocationPing(**payload.model_dump())
    db.add(ping)
    db.commit()
    db.refresh(ping)
    check_geofences(trip, payload.lat, payload.lng, db)
    return ping

@router.get("/live", response_model=List[LiveLocation])
def live_positions(db: Session = Depends(get_db)):
    """Latest GPS ping for every active trip."""
    from app.models.models import TripStatus
    active = db.query(Trip).filter(
        Trip.status.in_([TripStatus.LOADED, TripStatus.IN_TRANSIT])
    ).all()
    result = []
    for trip in active:
        if trip.locations:
            last = trip.locations[-1]
            result.append(LiveLocation(
                trip_id=trip.id,
                lat=last.lat,
                lng=last.lng,
                speed_kmh=last.speed_kmh,
                bearing=last.bearing,
                timestamp=last.timestamp,
                status=trip.status,
            ))
    return result

@router.get("/{trip_id}/route", response_model=List[LocationPingOut])
def get_route(trip_id: int, db: Session = Depends(get_db)):
    """Full breadcrumb trail for a trip."""
    return db.query(LocationPing)\
        .filter(LocationPing.trip_id == trip_id)\
        .order_by(LocationPing.timestamp)\
        .all()

@router.get("/{trip_id}/latest", response_model=LocationPingOut)
def latest_ping(trip_id: int, db: Session = Depends(get_db)):
    ping = db.query(LocationPing)\
        .filter(LocationPing.trip_id == trip_id)\
        .order_by(LocationPing.timestamp.desc())\
        .first()
    if not ping:
        raise HTTPException(status_code=404, detail="No location data yet")
    return ping
