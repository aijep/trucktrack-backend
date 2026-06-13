from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.models import Trip, TripStatus, Checkpoint
from app.schemas.schemas import TripCreate, TripOut, TripSummary, StatusUpdate, CheckpointCreate, CheckpointOut

router = APIRouter()

@router.post("/", response_model=TripOut)
def create_trip(payload: TripCreate, db: Session = Depends(get_db)):
    trip = Trip(**payload.model_dump())
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip

@router.get("/", response_model=List[TripSummary])
def list_trips(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Trip).order_by(Trip.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/active", response_model=List[TripOut])
def active_trips(db: Session = Depends(get_db)):
    return db.query(Trip).filter(
        Trip.status.in_([TripStatus.LOADED, TripStatus.IN_TRANSIT])
    ).all()

@router.get("/{trip_id}", response_model=TripOut)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.patch("/{trip_id}/status", response_model=TripOut)
def update_status(trip_id: int, payload: StatusUpdate, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    now = datetime.now(timezone.utc)
    trip.status = payload.status
    if payload.status == TripStatus.LOADED:
        trip.loaded_at = now
    elif payload.status == TripStatus.IN_TRANSIT:
        trip.departed_at = now
    elif payload.status == TripStatus.ARRIVED:
        trip.arrived_at = now
    elif payload.status == TripStatus.UNLOADED:
        trip.unloaded_at = now
    elif payload.status == TripStatus.COMPLETED:
        trip.completed_at = now
    db.commit()
    db.refresh(trip)
    return trip

@router.post("/{trip_id}/checkpoints", response_model=CheckpointOut)
def add_checkpoint(trip_id: int, payload: CheckpointCreate, db: Session = Depends(get_db)):
    cp = Checkpoint(trip_id=trip_id, **payload.model_dump())
    db.add(cp)
    db.commit()
    db.refresh(cp)
    return cp

@router.get("/{trip_id}/checkpoints", response_model=List[CheckpointOut])
def list_checkpoints(trip_id: int, db: Session = Depends(get_db)):
    return db.query(Checkpoint).filter(Checkpoint.trip_id == trip_id).all()
