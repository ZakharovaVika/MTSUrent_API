from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging

from app.database import get_db
from app import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=schemas.Scooter, status_code=status.HTTP_201_CREATED)
def create_scooter(scooter: schemas.ScooterCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_scooter(db=db, scooter=scooter)
    except Exception as e:
        logger.error(f"Error creating scooter: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create scooter"
        )

@router.get("/", response_model=List[schemas.Scooter])
def read_scooters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_scooters(db, skip=skip, limit=limit)

@router.get("/{scooter_id}", response_model=schemas.Scooter)
def read_scooter(scooter_id: UUID, db: Session = Depends(get_db)):
    db_scooter = crud.get_scooter(db, scooter_id=scooter_id)
    if db_scooter is None:
        logger.warning(f"Scooter with id {scooter_id} not found")
        raise HTTPException(status_code=404, detail="Scooter not found")
    return db_scooter

@router.put("/{scooter_id}", response_model=schemas.Scooter)
def update_scooter(scooter_id: UUID, scooter: schemas.ScooterUpdate, db: Session = Depends(get_db)):
    db_scooter = crud.update_scooter(db, scooter_id=scooter_id, scooter_update=scooter)
    if db_scooter is None:
        raise HTTPException(status_code=404, detail="Scooter not found")
    return db_scooter

@router.delete("/{scooter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scooter(scooter_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_scooter(db, scooter_id=scooter_id)
    if not success:
        raise HTTPException(status_code=404, detail="Scooter not found")
    return None