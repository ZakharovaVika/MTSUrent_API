from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging

from app.database import get_db
from app import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=schemas.Ride, status_code=status.HTTP_201_CREATED)
def create_ride(ride: schemas.RideCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_ride(db=db, ride=ride)
    except Exception as e:
        logger.error(f"Error creating ride: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create ride"
        )

@router.get("/", response_model=List[schemas.Ride])
def read_rides(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_rides(db, skip=skip, limit=limit)

@router.get("/{ride_id}", response_model=schemas.Ride)
def read_ride(ride_id: UUID, db: Session = Depends(get_db)):
    db_ride = crud.get_ride(db, ride_id=ride_id)
    if db_ride is None:
        logger.warning(f"Ride with id {ride_id} not found")
        raise HTTPException(status_code=404, detail="Ride not found")
    return db_ride

@router.put("/{ride_id}", response_model=schemas.Ride)
def update_ride(ride_id: UUID, ride: schemas.RideUpdate, db: Session = Depends(get_db)):
    db_ride = crud.update_ride(db, ride_id=ride_id, ride_update=ride)
    if db_ride is None:
        raise HTTPException(status_code=404, detail="Ride not found")
    return db_ride

@router.delete("/{ride_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ride(ride_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_ride(db, ride_id=ride_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ride not found")
    return None

@router.post("/{ride_id}/complete", response_model=schemas.Ride)
def complete_ride(ride_id: UUID, end_lat: float, end_lon: float, distance: float, cost: float, db: Session = Depends(get_db)):
    try:
        return crud.complete_ride(db=db, ride_id=ride_id, end_lat=end_lat, end_lon=end_lon, distance=distance, cost=cost)
    except Exception as e:
        logger.error(f"Error completing ride: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not complete ride"
        )