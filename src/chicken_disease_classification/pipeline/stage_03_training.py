from src.chicken_disease_classification.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.chicken_disease_classification.config.configuration import ConfigurationManager
from src.chicken_disease_classification.components.training import Training
from src.chicken_disease_classification import logger


STAGE_NAME= 'Final Model Training Pipeline'

class ModelTrainingPipeline():
    def __init__(self):
        pass
    def main(self):
        try:
            
            config_manager= ConfigurationManager(config_file_path= CONFIG_FILE_PATH,params_file_path=PARAMS_FILE_PATH)
            # prepare_callbacks_config= config_manager.get_prepare_callbacks_config()
           
            training_config= config_manager.training_config()
            training_component= Training(config= training_config)
            training_component.get_base_model()
            training_component.preprocess_data()
            training_component.build_additional_parameters()
            model= Training.train_model(model=training_component.model,
                                dataloaders= training_component.image_dataloaders,
                                criterion=training_component.criterion,
                                optimiser=training_component.optimiser_conv,
                                scheduler= training_component.exp_decay_lr_scheduler,
                                dataset_sizes=training_component.dataset_sizes,
                                num_epochs= training_component.config.params_epochs)
            Training.save_model(training_component.config.trained_model_path,model= model)

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

