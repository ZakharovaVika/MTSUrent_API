import logging
import os
import json
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from config.etl_config import etl_config

logger = logging.getLogger(__name__)

class DataLoader:
    """Загрузчик: конвертирует dict->schemas и вызывает crud.create_*"""

    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def load_users(self, rows: List[Dict[str, Any]], stats: Dict):
        for r in rows:
            try:
                data = schemas.UserCreate(**r)
                crud.create_user(self.db, data)
                stats['created'] += 1
            except Exception as e:
                logger.exception("Error inserting user")
                stats['errors'].append(str(e))

    def load_scooters(self, rows, stats):
        for r in rows:
            try:
                data = schemas.ScooterCreate(**r)
                crud.create_scooter(self.db, data)
                stats['created'] += 1
            except Exception as e:
                logger.exception("Error inserting scooter")
                stats['errors'].append(str(e))

    def load_tariffs(self, rows, stats):
        for r in rows:
            try:
                data = schemas.TariffCreate(**r)
                crud.create_tariff(self.db, data)
                stats['created'] += 1
            except Exception as e:
                logger.exception("Error inserting tariff")
                stats['errors'].append(str(e))

    def load_rides(self, rows, stats):
        for r in rows:
            try:
                data = schemas.RideCreate(**r)
                crud.create_ride(self.db, data)
                stats['created'] += 1
            except Exception as e:
                logger.exception("Error inserting ride")
                stats['errors'].append(str(e))

    def load_payments(self, rows, stats):
        for r in rows:
            try:
                data = schemas.PaymentCreate(**r)
                crud.create_payment(self.db, data)
                stats['created'] += 1
            except Exception as e:
                logger.exception("Error inserting payment")
                stats['errors'].append(str(e))

    def close(self):
        try:
            self.db.close()
        except:
            pass
