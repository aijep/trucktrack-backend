from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Driver
from app.schemas.schemas import DriverCreate, DriverOut

router = APIRouter()

@router.post("/", response_model=DriverOut)
def create(payload: DriverCreate, db: Session = Depends(get_db)):
    d = Driver(**payload.model_dump())
    db.add(d); db.commit(); db.refresh(d)
    return d

@router.get("/", response_model=List[DriverOut])
def list_all(db: Session = Depends(get_db)):
    return db.query(Driver).filter(Driver.is_active == True).all()
