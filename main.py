from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
import logging
import uvicorn
import os
import uuid
from typing import Dict, Any

from app.database import engine, get_db, SessionLocal
from app import models
from app.routers import (
    users, rides, tariffs, service_staff,
    scooters_statuses, scooters, payments,
    payments_statuses, maintenance
)


# Настройка логгера для main.py
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="MTS Urent API",
    description="REST API for MTS Urent",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(rides.router, prefix="/api/rides", tags=["rides"])
app.include_router(scooters.router, prefix="/api/scooters", tags=["scooters"])
app.include_router(tariffs.router, prefix="/api/tariffs", tags=["tariffs"])
app.include_router(service_staff.router, prefix="/api/service-staff", tags=["service-staff"])
app.include_router(maintenance.router, prefix="/api/maintenance", tags=["maintenance"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(scooters_statuses.router, prefix="/api/scooters-statuses", tags=["scooters-statuses"])
app.include_router(payments_statuses.router, prefix="/api/payments-statuses", tags=["payments-statuses"])


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "MTS Urent API ",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Health check endpoint
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query to check database connection
        db.execute(text('SELECT 1'))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Database connection failed")




if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )