import os
from typing import List
import pandas as pd
import logging
from config.etl_config import etl_config

logger = logging.getLogger(__name__)

class DataExtractor:
    """Извлекает табличные файлы (CSV / XLSX) из папки input"""

    def __init__(self, input_dir: str = None):
        self.input_dir = input_dir or etl_config.INPUT_DIR
        self.supported_ext = ['.csv', '.xlsx', '.xls']

    def list_available_files(self) -> List[str]:
        files = []
        for fname in os.listdir(self.input_dir):
            if any(fname.lower().endswith(ext) for ext in self.supported_ext):
                files.append(os.path.join(self.input_dir, fname))
        logger.info(f"Найдено файлов для обработки: {len(files)}")
        return files

    def extract_data(self, file_path: str, sheet_name: str = None) -> pd.DataFrame:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(file_path)
        else:
            # Excel: если sheet_name указан — читаем только его, иначе - первый
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        # базовая нормализация колонок
        df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]
        df = df.dropna(how='all')
        logger.info(f"Извлечено {len(df)} строк из {file_path}")
        return df

    # Удобные методы для сущностей — предполагается, что входные файлы именованы:
    # users_..., scooters_..., tariffs_..., rides_..., payments_..., maintenance_...
    def extract_entity(self, file_path: str) -> (str, pd.DataFrame):
        """Определяет сущность по имени файла и возвращает (entity, df)"""
        name = os.path.basename(file_path).lower()
        df = self.extract_data(file_path)
        if 'user' in name or 'users' in name:
            return 'users', df
        if 'scooter' in name or 'scooters' in name:
            return 'scooters', df
        if 'tariff' in name or 'tariffs' in name:
            return 'tariffs', df
        if 'ride' in name or 'rides' in name:
            return 'rides', df
        if 'payment' in name or 'payments' in name:
            return 'payments', df
        if 'maintenance' in name or 'maintenances' in name:
            return 'maintenance', df
        # fallback
        return 'unknown', df
