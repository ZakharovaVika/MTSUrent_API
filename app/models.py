from sqlalchemy import Column, String, Integer, DateTime, Date, Numeric, SmallInteger, Text, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Dictionary_ScooterStatus(Base):
    __tablename__ = 'Dictionary_ScooterStatus'

    status_code = Column(String(20), primary_key=True)
    status_name = Column(String(50), nullable=False)
    description = Column(String(200))

    # Relationships
    scooters = relationship("Scooter", back_populates="status")


class Dictionary_PaymentStatus(Base):
    __tablename__ = 'Dictionary_PaymentStatus'

    status_code = Column(String(20), primary_key=True)
    status_name = Column(String(50), nullable=False)
    description = Column(String(200))

    # Relationships
    payments = relationship("Payment", back_populates="payment_status")


class User(Base):
    __tablename__ = 'User'

    user_id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    phone_number = Column(String(15), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100))
    date_of_birth = Column(Date)
    registration_date = Column(DateTime, nullable=False, server_default=func.getutcdate())
    rating = Column(Numeric(3, 2), nullable=False, server_default='0.00')

    # Relationships
    rides = relationship("Ride", back_populates="user")

    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 5', name='CHK_User_Rating'),
        CheckConstraint('driver_license_verified IN (0, 1)', name='CHK_User_LicenseVerified'),
    )


class Scooter(Base):
    __tablename__ = 'Scooter'

    scooter_id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    model = Column(String(100), nullable=False)
    manufacture_date = Column(Date, nullable=False)
    current_battery = Column(SmallInteger, nullable=False, server_default='100')
    gps_latitude = Column(Numeric(10, 8))
    gps_longitude = Column(Numeric(11, 8))
    status_code = Column(String(20), ForeignKey('Dictionary_ScooterStatus.status_code'), nullable=False)
    qr_code = Column(String(100), nullable=False, unique=True)
    created_datetime = Column(DateTime, nullable=False, server_default=func.getutcdate())

    # Relationships
    status = relationship("Dictionary_ScooterStatus", back_populates="scooters")
    rides = relationship("Ride", back_populates="scooter")
    maintenances = relationship("Maintenance", back_populates="scooter")

    __table_args__ = (
        CheckConstraint('current_battery >= 0 AND current_battery <= 100', name='CHK_Scooter_Battery'),
    )


class Tariff(Base):
    __tablename__ = 'Tariff'

    tariff_id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    tariff_name = Column(String(100), nullable=False)
    unlock_fee = Column(Numeric(10, 2), nullable=False, server_default='0')
    rate_per_minute = Column(Numeric(10, 2), nullable=False, server_default='0')
    rate_per_km = Column(Numeric(10, 2))
    is_active = Column(SmallInteger, nullable=False, server_default='1')
    created_datetime = Column(DateTime, nullable=False, server_default=func.getutcdate())

    # Relationships
    rides = relationship("Ride", back_populates="tariff")

    __table_args__ = (
        CheckConstraint('unlock_fee >= 0', name='CHK_Tariff_UnlockFee'),
        CheckConstraint('rate_per_minute >= 0', name='CHK_Tariff_RatePerMinute'),
        CheckConstraint('is_active IN (0, 1)', name='CHK_Tariff_IsActive'),
    )


class ServiceStaff(Base):
    __tablename__ = 'ServiceStaff'

    staff_id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    created_datetime = Column(DateTime, nullable=False, server_default=func.getutcdate())

    # Relationships
    maintenances = relationship("Maintenance", back_populates="staff")


class Ride(Base):
    __tablename__ = 'Ride'

    ride_id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    start_time = Column(DateTime, nullable=False, server_default=func.getutcdate())
    end_time = Column(DateTime)
    start_latitude = Column(Numeric(10, 8), nullable=False)
    start_longitude = Column(Numeric(11, 8), nullable=False)
    end_latitude = Column(Numeric(10, 8))
    end_longitude = Column(Numeric(11, 8))
    distance = Column(Numeric(8, 2), nullable=False, server_default='0')
    ride_cost = Column(Numeric(10, 2), nullable=False, server_default='0')
    user_id = Column(UNIQUEIDENTIFIER, ForeignKey('User.user_id'), nullable=False)
    scooter_id = Column(UNIQUEIDENTIFIER, ForeignKey('Scooter.scooter_id'), nullable=False)
    tariff_id = Column(UNIQUEIDENTIFIER, ForeignKey('Tariff.tariff_id'), nullable=False)
    created_datetime = Column(DateTime, nullable=False, server_default=func.getutcdate())

    # Relationships
    user = relationship("User", back_populates="rides")
    scooter = relationship("Scooter", back_populates="rides")
    tariff = relationship("Tariff", back_populates="rides")
    payment = relationship("Payment", back_populates="ride", uselist=False)

    __table_args__ = (
        CheckConstraint('distance >= 0', name='CHK_Ride_Distance'),
        CheckConstraint('ride_cost >= 0', name='CHK_Ride_Cost'),
        CheckConstraint('end_time IS NULL OR end_time > start_time', name='CHK_Ride_Dates'),
    )


class Payment(Base):
    __tablename__ = 'Payment'

    payment_id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False, server_default=func.getutcdate())
    payment_method = Column(String(50), nullable=False)
    status_code = Column(String(20), ForeignKey('Dictionary_PaymentStatus.status_code'), nullable=False)
    ride_id = Column(UNIQUEIDENTIFIER, ForeignKey('Ride.ride_id'), nullable=False, unique=True)
    created_datetime = Column(DateTime, nullable=False, server_default=func.getutcdate())

    # Relationships
    payment_status = relationship("Dictionary_PaymentStatus", back_populates="payments")
    ride = relationship("Ride", back_populates="payment")

    __table_args__ = (
        CheckConstraint('amount > 0', name='CHK_Payment_Amount'),
    )


class Maintenance(Base):
    __tablename__ = 'Maintenance'

    maintenance_id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    maintenance_type = Column(String(50), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    completed_date = Column(Date)
    description = Column(String(500))
    status = Column(String(20), nullable=False, server_default='scheduled')
    scooter_id = Column(UNIQUEIDENTIFIER, ForeignKey('Scooter.scooter_id'), nullable=False)
    staff_id = Column(UNIQUEIDENTIFIER, ForeignKey('ServiceStaff.staff_id'), nullable=False)
    created_datetime = Column(DateTime, nullable=False, server_default=func.getutcdate())

    # Relationships
    scooter = relationship("Scooter", back_populates="maintenances")
    staff = relationship("ServiceStaff", back_populates="maintenances")

    __table_args__ = (
        CheckConstraint('completed_date IS NULL OR completed_date >= scheduled_date', name='CHK_Maintenance_Dates'),
    )