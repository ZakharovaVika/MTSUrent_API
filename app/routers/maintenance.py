from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging

from app.database import get_db
from app import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=schemas.Maintenance, status_code=status.HTTP_201_CREATED)
def create_maintenance(maintenance: schemas.MaintenanceCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_maintenance(db=db, maintenance=maintenance)
    except Exception as e:
        logger.error(f"Error creating maintenance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create maintenance"
        )

@router.get("/", response_model=List[schemas.Maintenance])
def read_maintenances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_maintenances(db, skip=skip, limit=limit)

@router.get("/{maintenance_id}", response_model=schemas.Maintenance)
def read_maintenance(maintenance_id: UUID, db: Session = Depends(get_db)):
    db_maintenance = crud.get_maintenance(db, maintenance_id=maintenance_id)
    if db_maintenance is None:
        logger.warning(f"Maintenance with id {maintenance_id} not found")
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return db_maintenance

@router.put("/{maintenance_id}", response_model=schemas.Maintenance)
def update_maintenance(maintenance_id: UUID, maintenance: schemas.MaintenanceUpdate, db: Session = Depends(get_db)):
    db_maintenance = crud.update_maintenance(db, maintenance_id=maintenance_id, maintenance_update=maintenance)
    if db_maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return db_maintenance

@router.delete("/{maintenance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_maintenance(maintenance_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_maintenance(db, maintenance_id=maintenance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return None

@router.post("/{maintenance_id}/complete", response_model=schemas.Maintenance)
def complete_maintenance(maintenance_id: UUID, db: Session = Depends(get_db)):
    try:
        return crud.complete_maintenance(db=db, maintenance_id=maintenance_id)
    except Exception as e:
        logger.error(f"Error completing maintenance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not complete maintenance"
        )