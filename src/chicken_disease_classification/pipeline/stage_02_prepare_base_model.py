from src.chicken_disease_classification.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.chicken_disease_classification.config.configuration import ConfigurationManager
from src.chicken_disease_classification.components.prepare_base_model import PrepareBaseModel
from src.chicken_disease_classification import logger

STAGE_NAME= "Prepare base model"

class PrepareBaseModelTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            config= ConfigurationManager(config_file_path= CONFIG_FILE_PATH, params_file_path=PARAMS_FILE_PATH)
            prepare_base_model_config= config.get_prepare_base_model_config()
            prepare_base_model= PrepareBaseModel(config= prepare_base_model_config)
            prepare_base_model.get_base_model()
            prepare_base_model.update_base_model()
        except Exception as e:
            raise e


if __name__=="__main__":
    try:
        pass
        logger.info(f"*************** Stage: {STAGE_NAME} started <<<<<<<<<<<<<<<<<<<<<<<<<<")
        obj= PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(f"*************** Stage: {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e



