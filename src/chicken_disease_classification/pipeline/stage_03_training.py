from src.chicken_disease_classification.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.chicken_disease_classification.config.configuration import ConfigurationManager
from src.chicken_disease_classification.components.prepare_callbacks import PrepareCallbacks
from src.chicken_disease_classification.components.training import Training
from src.chicken_disease_classification import logger
import tensorflow as tf

STAGE_NAME= 'Final Model Training Pipeline'

class ModelTrainingPipeline():
    def __init__(self):
        pass
    def main(self):
        try:
            
            config_manager= ConfigurationManager(config_file_path= CONFIG_FILE_PATH,params_file_path=PARAMS_FILE_PATH)
            prepare_callbacks_config= config_manager.get_prepare_callbacks_config()
            prepare_callback_component= PrepareCallbacks(config= prepare_callbacks_config)
            callback_list= prepare_callback_component.get_tb_ckpt_callbacks()

            training_config= config_manager.training_config()
            training_component= Training(config= training_config)
            training_component.get_base_model()
            training_component.train_valid_generator()
            training_component.train(
                callback_list= callback_list
            )

        except Exception as e:
            raise e
        
if __name__=="__main__":
    try:
        pass
        logger.info(f"*************** Stage: {STAGE_NAME} started <<<<<<<<<<<<<<<<<<<<<<<<<<")
        obj= ModelTrainingPipeline()
        obj.main()
        logger.info(f"*************** Stage: {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<<<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e

