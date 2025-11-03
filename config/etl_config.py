import os
from dataclasses import dataclass
from typing import Dict

@dataclass
class ETLConfig:
    # Пути
    INPUT_DIR: str = "data/input"
    OUTPUT_DIR: str = "data/output"
    PROCESSED_DIR: str = "data/processed"
    ERRORS_DIR: str = "data/errors"

    # Параметры обработки
    CHUNK_SIZE: int = 1000
    MAX_ERRORS: int = 100

    # Примеры отображений (можно расширить)
    SCOOTER_STATUS_MAPPING: Dict[str,str] = None
    PAYMENT_STATUS_MAPPING: Dict[str,str] = None

    def __post_init__(self):
        # базовые отображения — при необходимости заменять
        self.SCOOTER_STATUS_MAPPING = {
            'available': 'available',
            'in_use': 'in_use',
            'maintenance': 'maintenance',
            'reserved': 'reserved',
            'offline': 'offline',
        }
        self.PAYMENT_STATUS_MAPPING = {
            'paid': 'paid',
            'pending': 'pending',
            'failed': 'failed',
            'refunded': 'refunded'
        }

    def ensure_directories(self):
        for d in [self.INPUT_DIR, self.OUTPUT_DIR, self.PROCESSED_DIR, self.ERRORS_DIR]:
            os.makedirs(d, exist_ok=True)

# Глобальная конфигурация
etl_config = ETLConfig()
etl_config.ensure_directories()
