from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import logging
from app import models, schemas

logger = logging.getLogger(__name__)

# User CRUD
def get_user(db: Session, user_id: UUID) -> Optional[models.User]:
    logger.info(f"Fetching user with ID: {user_id}")
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    logger.info(f"Fetching users with skip: {skip}, limit: {limit}")
    return db.query(models.User).order_by(models.User.registration_date.desc()).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    logger.info(f"Creating user: {user.first_name} {user.last_name}")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with ID: {db_user.user_id}")
    return db_user

def update_user(db: Session, user_id: UUID, user_update: schemas.UserUpdate) -> Optional[models.User]:
    logger.info(f"Updating user with ID: {user_id}")
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User with ID {user_id} updated successfully")
    else:
        logger.warning(f"User with ID {user_id} not found for update")
    return db_user

def delete_user(db: Session, user_id: UUID) -> bool:
    logger.info(f"Deleting user with ID: {user_id}")
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        logger.info(f"User with ID {user_id} deleted successfully")
        return True
    logger.warning(f"User with ID {user_id} not found for deletion")
    return False

# Scooter CRUD
def get_scooter(db: Session, scooter_id: UUID) -> Optional[models.Scooter]:
    logger.info(f"Fetching scooter with ID: {scooter_id}")
    return db.query(models.Scooter).filter(models.Scooter.scooter_id == scooter_id).first()

def get_scooters(db: Session, skip: int = 0, limit: int = 100) -> List[models.Scooter]:
    logger.info(f"Fetching scooters with skip: {skip}, limit: {limit}")
    return db.query(models.Scooter).order_by(models.Scooter.created_datetime.desc()).offset(skip).limit(limit).all()

def create_scooter(db: Session, scooter: schemas.ScooterCreate) -> models.Scooter:
    logger.info(f"Creating scooter: {scooter.model}")
    db_scooter = models.Scooter(**scooter.dict())
    db.add(db_scooter)
    db.commit()
    db.refresh(db_scooter)
    logger.info(f"Scooter created with ID: {db_scooter.scooter_id}")
    return db_scooter

def update_scooter(db: Session, scooter_id: UUID, scooter_update: schemas.ScooterUpdate) -> Optional[models.Scooter]:
    logger.info(f"Updating scooter with ID: {scooter_id}")
    db_scooter = get_scooter(db, scooter_id)
    if db_scooter:
        update_data = scooter_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_scooter, field, value)
        db.commit()
        db.refresh(db_scooter)
        logger.info(f"Scooter with ID {scooter_id} updated successfully")
    else:
        logger.warning(f"Scooter with ID {scooter_id} not found for update")
    return db_scooter

def delete_scooter(db: Session, scooter_id: UUID) -> bool:
    logger.info(f"Deleting scooter with ID: {scooter_id}")
    db_scooter = get_scooter(db, scooter_id)
    if db_scooter:
        db.delete(db_scooter)
        db.commit()
        logger.info(f"Scooter with ID {scooter_id} deleted successfully")
        return True
    logger.warning(f"Scooter with ID {scooter_id} not found for deletion")
    return False

# Tariff CRUD
def get_tariff(db: Session, tariff_id: UUID) -> Optional[models.Tariff]:
    logger.info(f"Fetching tariff with ID: {tariff_id}")
    return db.query(models.Tariff).filter(models.Tariff.tariff_id == tariff_id).first()

def get_tariffs(db: Session, skip: int = 0, limit: int = 100) -> List[models.Tariff]:
    logger.info(f"Fetching tariffs with skip: {skip}, limit: {limit}")
    return db.query(models.Tariff).order_by(models.Tariff.created_datetime.desc()).offset(skip).limit(limit).all()

def create_tariff(db: Session, tariff: schemas.TariffCreate) -> models.Tariff:
    logger.info(f"Creating tariff: {tariff.tariff_name}")
    db_tariff = models.Tariff(**tariff.dict())
    db.add(db_tariff)
    db.commit()
    db.refresh(db_tariff)
    logger.info(f"Tariff created with ID: {db_tariff.tariff_id}")
    return db_tariff

def update_tariff(db: Session, tariff_id: UUID, tariff_update: schemas.TariffUpdate) -> Optional[models.Tariff]:
    logger.info(f"Updating tariff with ID: {tariff_id}")
    db_tariff = get_tariff(db, tariff_id)
    if db_tariff:
        update_data = tariff_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tariff, field, value)
        db.commit()
        db.refresh(db_tariff)
        logger.info(f"Tariff with ID {tariff_id} updated successfully")
    else:
        logger.warning(f"Tariff with ID {tariff_id} not found for update")
    return db_tariff

def delete_tariff(db: Session, tariff_id: UUID) -> bool:
    logger.info(f"Deleting tariff with ID: {tariff_id}")
    db_tariff = get_tariff(db, tariff_id)
    if db_tariff:
        db.delete(db_tariff)
        db.commit()
        logger.info(f"Tariff with ID {tariff_id} deleted successfully")
        return True
    logger.warning(f"Tariff with ID {tariff_id} not found for deletion")
    return False

# Ride CRUD
def get_ride(db: Session, ride_id: UUID) -> Optional[models.Ride]:
    logger.info(f"Fetching ride with ID: {ride_id}")
    return db.query(models.Ride).filter(models.Ride.ride_id == ride_id).first()

def get_rides(db: Session, skip: int = 0, limit: int = 100) -> List[models.Ride]:
    logger.info(f"Fetching rides with skip: {skip}, limit: {limit}")
    return db.query(models.Ride).order_by(models.Ride.start_time.desc()).offset(skip).limit(limit).all()

def create_ride(db: Session, ride: schemas.RideCreate) -> models.Ride:
    logger.info(f"Creating ride for user: {ride.user_id}")
    db_ride = models.Ride(**ride.dict())
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    logger.info(f"Ride created with ID: {db_ride.ride_id}")
    return db_ride

def update_ride(db: Session, ride_id: UUID, ride_update: schemas.RideUpdate) -> Optional[models.Ride]:
    logger.info(f"Updating ride with ID: {ride_id}")
    db_ride = get_ride(db, ride_id)
    if db_ride:
        update_data = ride_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ride, field, value)
        db.commit()
        db.refresh(db_ride)
        logger.info(f"Ride with ID {ride_id} updated successfully")
    else:
        logger.warning(f"Ride with ID {ride_id} not found for update")
    return db_ride

def delete_ride(db: Session, ride_id: UUID) -> bool:
    logger.info(f"Deleting ride with ID: {ride_id}")
    db_ride = get_ride(db, ride_id)
    if db_ride:
        db.delete(db_ride)
        db.commit()
        logger.info(f"Ride with ID {ride_id} deleted successfully")
        return True
    logger.warning(f"Ride with ID {ride_id} not found for deletion")
    return False

# Payment CRUD
def get_payment(db: Session, payment_id: UUID) -> Optional[models.Payment]:
    logger.info(f"Fetching payment with ID: {payment_id}")
    return db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()

def get_payments(db: Session, skip: int = 0, limit: int = 100) -> List[models.Payment]:
    logger.info(f"Fetching payments with skip: {skip}, limit: {limit}")
    return db.query(models.Payment).order_by(models.Payment.payment_date.desc()).offset(skip).limit(limit).all()

def create_payment(db: Session, payment: schemas.PaymentCreate) -> models.Payment:
    logger.info(f"Creating payment for ride: {payment.ride_id}")
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    logger.info(f"Payment created with ID: {db_payment.payment_id}")
    return db_payment

def update_payment(db: Session, payment_id: UUID, payment_update: schemas.PaymentUpdate) -> Optional[models.Payment]:
    logger.info(f"Updating payment with ID: {payment_id}")
    db_payment = get_payment(db, payment_id)
    if db_payment:
        update_data = payment_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_payment, field, value)
        db.commit()
        db.refresh(db_payment)
        logger.info(f"Payment with ID {payment_id} updated successfully")
    else:
        logger.warning(f"Payment with ID {payment_id} not found for update")
    return db_payment

def delete_payment(db: Session, payment_id: UUID) -> bool:
    logger.info(f"Deleting payment with ID: {payment_id}")
    db_payment = get_payment(db, payment_id)
    if db_payment:
        db.delete(db_payment)
        db.commit()
        logger.info(f"Payment with ID {payment_id} deleted successfully")
        return True
    logger.warning(f"Payment with ID {payment_id} not found for deletion")
    return False

# Maintenance CRUD
def get_maintenance(db: Session, maintenance_id: UUID) -> Optional[models.Maintenance]:
    logger.info(f"Fetching maintenance with ID: {maintenance_id}")
    return db.query(models.Maintenance).filter(models.Maintenance.maintenance_id == maintenance_id).first()

def get_maintenances(db: Session, skip: int = 0, limit: int = 100) -> List[models.Maintenance]:
    logger.info(f"Fetching maintenances with skip: {skip}, limit: {limit}")
    return db.query(models.Maintenance).order_by(models.Maintenance.scheduled_date.desc()).offset(skip).limit(limit).all()

def create_maintenance(db: Session, maintenance: schemas.MaintenanceCreate) -> models.Maintenance:
    logger.info(f"Creating maintenance for scooter: {maintenance.scooter_id}")
    db_maintenance = models.Maintenance(**maintenance.dict())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    logger.info(f"Maintenance created with ID: {db_maintenance.maintenance_id}")
    return db_maintenance

def update_maintenance(db: Session, maintenance_id: UUID, maintenance_update: schemas.MaintenanceUpdate) -> Optional[models.Maintenance]:
    logger.info(f"Updating maintenance with ID: {maintenance_id}")
    db_maintenance = get_maintenance(db, maintenance_id)
    if db_maintenance:
        update_data = maintenance_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_maintenance, field, value)
        db.commit()
        db.refresh(db_maintenance)
        logger.info(f"Maintenance with ID {maintenance_id} updated successfully")
    else:
        logger.warning(f"Maintenance with ID {maintenance_id} not found for update")
    return db_maintenance

def delete_maintenance(db: Session, maintenance_id: UUID) -> bool:
    logger.info(f"Deleting maintenance with ID: {maintenance_id}")
    db_maintenance = get_maintenance(db, maintenance_id)
    if db_maintenance:
        db.delete(db_maintenance)
        db.commit()
        logger.info(f"Maintenance with ID {maintenance_id} deleted successfully")
        return True
    logger.warning(f"Maintenance with ID {maintenance_id} not found for deletion")
    return False

# ServiceStaff CRUD
def get_service_staff(db: Session, staff_id: UUID) -> Optional[models.ServiceStaff]:
    logger.info(f"Fetching service staff with ID: {staff_id}")
    return db.query(models.ServiceStaff).filter(models.ServiceStaff.staff_id == staff_id).first()

def get_all_service_staff(db: Session, skip: int = 0, limit: int = 100) -> List[models.ServiceStaff]:
    logger.info(f"Fetching service staff with skip: {skip}, limit: {limit}")
    return db.query(models.ServiceStaff).order_by(models.ServiceStaff.created_datetime.desc()).offset(skip).limit(limit).all()

def create_service_staff(db: Session, staff: schemas.ServiceStaffCreate) -> models.ServiceStaff:
    logger.info(f"Creating service staff: {staff.first_name} {staff.last_name}")
    db_staff = models.ServiceStaff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    logger.info(f"Service staff created with ID: {db_staff.staff_id}")
    return db_staff

def update_service_staff(db: Session, staff_id: UUID, staff_update: schemas.ServiceStaffUpdate) -> Optional[models.ServiceStaff]:
    logger.info(f"Updating service staff with ID: {staff_id}")
    db_staff = get_service_staff(db, staff_id)
    if db_staff:
        update_data = staff_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_staff, field, value)
        db.commit()
        db.refresh(db_staff)
        logger.info(f"Service staff with ID {staff_id} updated successfully")
    else:
        logger.warning(f"Service staff with ID {staff_id} not found for update")
    return db_staff

def delete_service_staff(db: Session, staff_id: UUID) -> bool:
    logger.info(f"Deleting service staff with ID: {staff_id}")
    db_staff = get_service_staff(db, staff_id)
    if db_staff:
        db.delete(db_staff)
        db.commit()
        logger.info(f"Service staff with ID {staff_id} deleted successfully")
        return True
    logger.warning(f"Service staff with ID {staff_id} not found for deletion")
    return False
# Dictionary CRUD operations
def get_scooter_statuses(db: Session, skip: int = 0, limit: int = 100) -> List[models.Dictionary_ScooterStatus]:
    logger.info("Fetching scooter statuses")
    return db.query(models.Dictionary_ScooterStatus).order_by(models.Dictionary_ScooterStatus.status_name).offset(skip).limit(limit).all()

def get_payment_statuses(db: Session, skip: int = 0, limit: int = 100) -> List[models.Dictionary_PaymentStatus]:
    logger.info("Fetching payment statuses")
    return db.query(models.Dictionary_PaymentStatus).order_by(models.Dictionary_PaymentStatus.status_name).offset(skip).limit(limit).all()