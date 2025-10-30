from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging

from app.database import get_db
from app import crud, schemas

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=schemas.Tariff, status_code=status.HTTP_201_CREATED)
def create_tariff(tariff: schemas.TariffCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_tariff(db=db, tariff=tariff)
    except Exception as e:
        logger.error(f"Error creating tariff: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create tariff"
        )

@router.get("/", response_model=List[schemas.Tariff])
def read_tariffs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tariffs(db, skip=skip, limit=limit)

@router.get("/{tariff_id}", response_model=schemas.Tariff)
def read_tariff(tariff_id: UUID, db: Session = Depends(get_db)):
    db_tariff = crud.get_tariff(db, tariff_id=tariff_id)
    if db_tariff is None:
        logger.warning(f"Tariff with id {tariff_id} not found")
        raise HTTPException(status_code=404, detail="Tariff not found")
    return db_tariff

@router.put("/{tariff_id}", response_model=schemas.Tariff)
def update_tariff(tariff_id: UUID, tariff: schemas.TariffUpdate, db: Session = Depends(get_db)):
    db_tariff = crud.update_tariff(db, tariff_id=tariff_id, tariff_update=tariff)
    if db_tariff is None:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return db_tariff

@router.delete("/{tariff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tariff(tariff_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_tariff(db, tariff_id=tariff_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return None