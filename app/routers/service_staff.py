from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging

from app.database import get_db
from app import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=schemas.ServiceStaff, status_code=status.HTTP_201_CREATED)
def create_service_staff(staff: schemas.ServiceStaffCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_service_staff(db=db, staff=staff)
    except Exception as e:
        logger.error(f"Error creating service staff: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create service staff"
        )

@router.get("/", response_model=List[schemas.ServiceStaff])
def read_service_staff(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_service_staff(db, skip=skip, limit=limit)

@router.get("/{staff_id}", response_model=schemas.ServiceStaff)
def read_service_staff_member(staff_id: UUID, db: Session = Depends(get_db)):
    db_staff = crud.get_service_staff(db, staff_id=staff_id)
    if db_staff is None:
        logger.warning(f"Service staff with id {staff_id} not found")
        raise HTTPException(status_code=404, detail="Service staff not found")
    return db_staff

@router.put("/{staff_id}", response_model=schemas.ServiceStaff)
def update_service_staff(staff_id: UUID, staff: schemas.ServiceStaffUpdate, db: Session = Depends(get_db)):
    db_staff = crud.update_service_staff(db, staff_id=staff_id, staff_update=staff)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Service staff not found")
    return db_staff

@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_staff(staff_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_service_staff(db, staff_id=staff_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service staff not found")
    return None