from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import trips, tracking, vehicles, drivers
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TruckTrack API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips.router,    prefix="/api/trips",    tags=["trips"])
app.include_router(tracking.router, prefix="/api/tracking", tags=["tracking"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["vehicles"])
app.include_router(drivers.router,  prefix="/api/drivers",  tags=["drivers"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
