from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.models import TripStatus

class DriverBase(BaseModel):
    name: str
    phone: str
    license_no: str

class DriverCreate(DriverBase): pass

class DriverOut(DriverBase):
    id: int
    is_active: bool
    class Config: from_attributes = True

class VehicleBase(BaseModel):
    plate_number: str
    model: Optional[str]
    capacity_ton: Optional[float]

class VehicleCreate(VehicleBase): pass

class VehicleOut(VehicleBase):
    id: int
    is_active: bool
    class Config: from_attributes = True

class TripCreate(BaseModel):
    driver_id: int
    vehicle_id: int
    source_name: str
    source_lat: float
    source_lng: float
    dest_name: str
    dest_lat: float
    dest_lng: float
    material_desc: Optional[str]
    load_weight_ton: Optional[float]

class CheckpointOut(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    radius_m: float
    arrived_at: Optional[datetime]
    departed_at: Optional[datetime]
    class Config: from_attributes = True

class LocationPingOut(BaseModel):
    id: int
    lat: float
    lng: float
    speed_kmh: float
    bearing: float
    timestamp: datetime
    class Config: from_attributes = True

class TripOut(BaseModel):
    id: int
    driver: DriverOut
    vehicle: VehicleOut
    source_name: str
    source_lat: float
    source_lng: float
    dest_name: str
    dest_lat: float
    dest_lng: float
    material_desc: Optional[str]
    load_weight_ton: Optional[float]
    status: TripStatus
    loaded_at: Optional[datetime]
    departed_at: Optional[datetime]
    arrived_at: Optional[datetime]
    unloaded_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    checkpoints: List[CheckpointOut] = []
    class Config: from_attributes = True

class TripSummary(BaseModel):
    id: int
    driver: DriverOut
    vehicle: VehicleOut
    source_name: str
    dest_name: str
    status: TripStatus
    created_at: datetime
    departed_at: Optional[datetime]
    arrived_at: Optional[datetime]
    class Config: from_attributes = True

class LocationPingCreate(BaseModel):
    trip_id: int
    lat: float
    lng: float
    speed_kmh: float = 0
    bearing: float = 0
    accuracy: Optional[float] = None

class LiveLocation(BaseModel):
    trip_id: int
    lat: float
    lng: float
    speed_kmh: float
    bearing: float
    timestamp: datetime
    status: TripStatus

class StatusUpdate(BaseModel):
    status: TripStatus

class CheckpointCreate(BaseModel):
    name: str
    lat: float
    lng: float
    radius_m: float = 200
