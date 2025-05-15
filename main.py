from src.chicken_disease_classification import logger
from src.chicken_disease_classification.pipeline.stage_01_data_ingestion import DataIngestionPipeline

STAGE_NAME= "01 Data Ingestion Stage"
try:
    pass
    logger.info(f"*************** Stage: {STAGE_NAME} started <<<<<<<<<<<<<<<<<<<<<<<<<<")
    obj= DataIngestionPipeline()
    obj.main()
    logger.info(f"*************** Stage: {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<<<<<<<<")
except Exception as e:
    logger.exception(e)
    raise e
logger.info("Logging has been set up successfully")