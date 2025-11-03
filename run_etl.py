import logging
from app.etl.orchestrator import ETLOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mt-surent-etl")

def main():
    orchestrator = ETLOrchestrator()
    report = orchestrator.run()
    logger.info("ETL завершён. Отчёт:")
    for f, stats in report.items():
        logger.info(f"{f} -> {stats}")

if __name__ == "__main__":
    main()
