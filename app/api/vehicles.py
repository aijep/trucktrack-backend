from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Vehicle
from app.schemas.schemas import VehicleCreate, VehicleOut

router = APIRouter()

@router.post("/", response_model=VehicleOut)
def create(payload: VehicleCreate, db: Session = Depends(get_db)):
    v = Vehicle(**payload.model_dump())
    db.add(v); db.commit(); db.refresh(v)
    return v

@router.get("/", response_model=List[VehicleOut])
def list_all(db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.is_active == True).all()
