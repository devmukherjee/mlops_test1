from src.chicken_disease_classification.entity.config_entity import DataIngestionConfig
from src.chicken_disease_classification.config.configuration import ConfigurationManager
from src.chicken_disease_classification.components.data_ingestion import DataIngestion
from src.chicken_disease_classification import logger
from src.chicken_disease_classification.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
STAGE_NAME= "01 data ingestion stage"

class DataIngestionPipeline:
    def __init__(self):
        # Lets get the pipeline
        pass
    
    def main(self):
        try:
            configuration_manager= ConfigurationManager(config_file_path= CONFIG_FILE_PATH, params_file_path= PARAMS_FILE_PATH)
            data_ingestion_config_entity= configuration_manager.get_data_ingestion_configuration()
            data_ingester_component= DataIngestion(config= data_ingestion_config_entity)
            data_ingester_component.download_file()
            data_ingester_component.extract_zip()
        except Exception as e:
            logger.error("Data Ingestion Setup failed with Exception: {e}")
            raise e
        
if __name__=="__main__":
    try:
        pass
        logger.info(f"*************** Stage: {STAGE_NAME} started <<<<<<<<<<<<<<<<<<<<<<<<<<")
        obj= DataIngestionPipeline()
        obj.main()
        logger.info(f"*************** Stage: {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e



    
