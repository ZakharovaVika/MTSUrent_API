import logging
import os
import shutil
from typing import Dict, Any, List
from app.etl.extractors import DataExtractor
from app.etl.transformers import DataTransformer
from app.etl.loaders import DataLoader
from app.etl.validators import UserValidator, ScooterValidator, RideValidator, PaymentValidator
from config.etl_config import etl_config

logger = logging.getLogger(__name__)

class ETLOrchestrator:
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
        self.validators = {
            'users': UserValidator(),
            'scooters': ScooterValidator(),
            'rides': RideValidator(),
            'payments': PaymentValidator()
        }

    def process_file(self, file_path: str):
        entity, df = self.extractor.extract_entity(file_path)
        logger.info(f"Обработка {file_path} как сущности {entity}, строк: {len(df)}")
        stats = {'total': 0, 'created': 0, 'errors': []}
        rows_to_load = []

        for _, raw in df.iterrows():
            row = raw.to_dict()
            stats['total'] += 1
            validator = self.validators.get(entity)
            if validator:
                ok, err = validator.validate(row)
                if not ok:
                    stats['errors'].append(err)
                    continue
            # трансформация
            transform_fn = getattr(self.transformer, f"transform_{entity}", None)
            if transform_fn:
                try:
                    out = transform_fn(row)
                    rows_to_load.append(out)
                except Exception as e:
                    logger.exception("Ошибка трансформации")
                    stats['errors'].append(str(e))
            else:
                stats['errors'].append(f"No transformer for {entity}")

        # загрузка
        loader_fn = getattr(self.loader, f"load_{entity}", None)
        if loader_fn and rows_to_load:
            loader_fn(rows_to_load, stats)
        import json
        if stats["errors"]:
            err_file = os.path.join(
                etl_config.ERRORS_DIR,
                os.path.basename(file_path) + ".errors.json"
            )
            with open(err_file, "w", encoding="utf-8") as f:
                json.dump(stats["errors"], f, ensure_ascii=False, indent=2)
            logger.warning(f"Ошибки сохранены в {err_file}")


        # по завершении — перемещаем файл в processed
        dest = os.path.join(etl_config.PROCESSED_DIR, os.path.basename(file_path))
        shutil.move(file_path, dest)
        logger.info(f"Файл {file_path} перемещён в {dest}")
        return stats

    def run(self):
        files = self.extractor.list_available_files()
        overall = {}
        for f in files:
            try:
                stats = self.process_file(f)
                overall[f] = stats
            except Exception as e:
                logger.exception(f"Failed processing {f}")
                # перемещаем в errors
                import shutil
                dest = os.path.join(etl_config.ERRORS_DIR, os.path.basename(f))
                shutil.move(f, dest)
                overall[f] = {'error': str(e)}
        self.loader.close()
        return overall
