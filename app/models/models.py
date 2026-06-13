from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class TripStatus(str, enum.Enum):
    PENDING   = "pending"
    LOADED    = "loaded"
    IN_TRANSIT= "in_transit"
    ARRIVED   = "arrived"
    UNLOADED  = "unloaded"
    COMPLETED = "completed"

class Driver(Base):
    __tablename__ = "drivers"
    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    phone      = Column(String(20), unique=True, nullable=False)
    license_no = Column(String(50), unique=True, nullable=False)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    trips      = relationship("Trip", back_populates="driver")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id           = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(20), unique=True, nullable=False)
    model        = Column(String(100))
    capacity_ton = Column(Float)
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    trips        = relationship("Trip", back_populates="vehicle")

class Trip(Base):
    __tablename__ = "trips"
    id              = Column(Integer, primary_key=True, index=True)
    driver_id       = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    vehicle_id      = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    source_name     = Column(String(200), nullable=False)
    source_lat      = Column(Float, nullable=False)
    source_lng      = Column(Float, nullable=False)
    dest_name       = Column(String(200), nullable=False)
    dest_lat        = Column(Float, nullable=False)
    dest_lng        = Column(Float, nullable=False)
    material_desc   = Column(Text)
    load_weight_ton = Column(Float)
    status          = Column(Enum(TripStatus), default=TripStatus.PENDING)
    loaded_at       = Column(DateTime(timezone=True))
    departed_at     = Column(DateTime(timezone=True))
    arrived_at      = Column(DateTime(timezone=True))
    unloaded_at     = Column(DateTime(timezone=True))
    completed_at    = Column(DateTime(timezone=True))
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    driver          = relationship("Driver",  back_populates="trips")
    vehicle         = relationship("Vehicle", back_populates="trips")
    locations       = relationship("LocationPing", back_populates="trip", order_by="LocationPing.timestamp")
    checkpoints     = relationship("Checkpoint", back_populates="trip")

class LocationPing(Base):
    __tablename__ = "location_pings"
    id        = Column(Integer, primary_key=True, index=True)
    trip_id   = Column(Integer, ForeignKey("trips.id"), nullable=False)
    lat       = Column(Float, nullable=False)
    lng       = Column(Float, nullable=False)
    speed_kmh = Column(Float, default=0)
    bearing   = Column(Float, default=0)
    accuracy  = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    trip      = relationship("Trip", back_populates="locations")

class Checkpoint(Base):
    __tablename__ = "checkpoints"
    id           = Column(Integer, primary_key=True, index=True)
    trip_id      = Column(Integer, ForeignKey("trips.id"), nullable=False)
    name         = Column(String(200), nullable=False)
    lat          = Column(Float, nullable=False)
    lng          = Column(Float, nullable=False)
    radius_m     = Column(Float, default=200)
    arrived_at   = Column(DateTime(timezone=True))
    departed_at  = Column(DateTime(timezone=True))
    trip         = relationship("Trip", back_populates="checkpoints")
